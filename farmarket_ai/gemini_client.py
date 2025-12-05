# gemini_client.py

import os
from typing import List, Dict, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
)


# -----------------------------------------------------------
# HELPER: Simple Distance Scoring (fallback when distance_km is missing)
# -----------------------------------------------------------
def score_distance(farmer_county: str, market_county: str) -> str:
    farmer = farmer_county.lower()
    market = market_county.lower()

    if farmer == market:
        return "very near you"
    if (
        (farmer.startswith("kajiado") and market.startswith("narok")) or
        (farmer.startswith("kakamega") and market.startswith("vihiga")) or
        (farmer.startswith("nyeri") and market.startswith("kirinyaga"))
    ):
        return "nearby your area"

    return "a bit farther but still reachable"


# -----------------------------------------------------------
# MULTI-LANGUAGE PROMPT BUILDER (normal case: 1–3 matched markets)
# -----------------------------------------------------------
def build_prompt(
    farmer_name: Optional[str],
    county: str,
    crop: str,
    markets: List[Dict],
    language: str
) -> str:

    name = farmer_name or "Mkulima"
    county_clean = county.strip()
    crop_clean = crop.strip()

    # Format markets deeply (distance, transport, profit, trend, tips)
    formatted = []
    for i, m in enumerate(markets, start=1):

        # Distance
        distance_text = (
            f"{m['distance_km']} km away"
            if "distance_km" in m
            else score_distance(county_clean, m["county"])
        )

        transport_text = f"Transport: {m.get('transport_cost', 'N/A')} KES"
        profit_text = f"Effective Profit: {m.get('effective_profit', 'N/A')} KES"
        trend_text = m.get("trend_message", "No price trend information available.")

        # Transport tips (list)
        tips_list = m.get("tips", [])
        if tips_list:
            tips_text = "\n".join([f"   - {t}" for t in tips_list])
        else:
            tips_text = "   - No transport advice available"

        formatted.append(
            f"{i}. {m['market']} – Price: {m['retail_price']} KES, "
            f"{distance_text}, {transport_text}, {profit_text}\n"
            f"   Trend: {trend_text}\n"
            f"   Transport Tips:\n{tips_text}"
        )

    markets_text = "\n".join(formatted)

    # Language toggles
    include_sw = (language == "sw" or language == "both")
    include_local = (language == "local" or language == "both")

    base = f"""
You are an agricultural assistant helping a Kenyan farmer decide the best market to sell produce.

Address the farmer directly by name.

FARMER DETAILS:
- Name: {name}
- County: {county_clean}
- Crop: {crop_clean}

Below are the ONLY 3 markets selected by the system.
Each includes: retail price, distance estimate, transport cost, effective profit,
a price trend insight, and transport-saving tips.

{markets_text}

YOUR TASK:
1. Speak directly to {name}, e.g. "**{name}**, the nearest and most profitable market for you is...".
2. Choose **ONE best market** using:
   - Highest effective profit
   - Lower transport cost
   - Shorter distance
   - Trend information (rising, falling, stable)
3. Explain the recommendation in **2–3 simple English sentences**.
4. Give a **one-sentence insight** for each of the other two markets.
5. Provide practical advice such as:
   - Best time to sell (morning, market day)
   - How transport affects profit
   - Ways to reduce cost (shared transport, early departure)
6. DO NOT create new markets or new data.

PRIMARY LANGUAGE:
Your main explanation MUST be in **English**.
"""

    if include_sw:
        base += f"""

OPTIONAL SWAHILI VERSION:
Give a 2–3 sentence Swahili summary after the English one.
Address {name} directly.
"""

    if include_local:
        base += f"""

OPTIONAL LOCAL DIALECT:
Provide ONE short respectful sentence in a dialect suitable for the farmer's county.
"""

    base += """
WHATSAPP FORMATTING RULES:
- Clean line breaks.
- Allowed: bullets (•), bold text (**John**)
- Keep message short, clear, and helpful.
"""

    return base.strip()


# -----------------------------------------------------------
# FALLBACK PROMPT WHEN NO MATCHING MARKETS FOUND
# -----------------------------------------------------------
def build_fallback_prompt(
    farmer_name: Optional[str],
    county: str,
    crop: str,
    language: str
):
    name = farmer_name or "Mkulima"

    base = f"""
You are an agricultural advisor assisting a Kenyan farmer.

We could NOT find specific market price data for:
- Farmer: {name}
- County: {county}
- Crop: {crop}

YOUR TASK:
1. Give **helpful, practical guidance in English**, even though data is missing.
2. DO NOT invent any markets or prices.
3. Give 3–4 steps the farmer can take today to find a good selling point, such as:
   - Checking nearby trading centers
   - Asking transporters about demand in different markets
   - Visiting common regional markets
   - Comparing buyer offers early in the morning
4. Mention how to choose a market based on:
   - Distance
   - Transport cost
   - Demand patterns
5. Address {name} directly and keep the tone friendly.

"""

    if language in ["sw", "both"]:
        base += f"""
OPTIONAL SWAHILI VERSION:
Provide a short 2–3 sentence Swahili summary. Do NOT create fake prices or markets.
"""

    if language in ["local", "both"]:
        base += """
OPTIONAL LOCAL DIALECT:
Give ONE short respectful sentence in an appropriate dialect.
"""

    return base.strip()


# -----------------------------------------------------------
# GEMINI REQUEST HANDLER (now includes fallback logic)
# -----------------------------------------------------------
async def generate_explanation(
    farmer_name: Optional[str],
    county: str,
    crop: str,
    markets: List[Dict],
    language: str = "en"
) -> str:

    # -------------------------------------------------------
    # SOFT FALLBACK → NO MATCHING MARKETS
    # -------------------------------------------------------
    if not markets:
        prompt = build_fallback_prompt(farmer_name, county, crop, language)

        # If offline → minimal fallback
        if not GEMINI_API_KEY:
            return (
                f"{farmer_name or 'Mkulima'}, we could not find price data for {crop}. "
                "Try nearby markets, compare buyer offers early, and factor transport cost."
            )

        # Ask Gemini for general guidance
        try:
            headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}
            payload = {"contents": [{"parts": [{"text": prompt}]}]}

            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(GEMINI_URL, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()

            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
            return text.strip() or "General advice unavailable."

        except Exception:
            return (
                f"{farmer_name or 'Mkulima'}, although we have no data, "
                "you can check nearby markets, compare prices, and choose the location "
                "with the highest demand and lowest transport cost."
            )

    # -------------------------------------------------------
    # NORMAL CASE → MARKETS FOUND
    # -------------------------------------------------------
    if not GEMINI_API_KEY:
        best = markets[0]
        return (
            f"{farmer_name}, based on available data, the best market is {best['market']} "
            f"with a price of {best['retail_price']} KES."
        )

    prompt = build_prompt(farmer_name, county, crop, markets, language)

    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    # Request AI response
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(GEMINI_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        text = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )
        return text.strip() or "No explanation generated."

    except Exception:
        best = markets[0]
        return (
            f"{farmer_name}, the recommended market is {best['market']} "
            f"with a price of {best['retail_price']} KES. "
            "Consider distance and transport before deciding."
        )
