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
# HELPER: Simple Distance Scoring (fallback when distance_km is not provided)
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
# MULTI-LANGUAGE PROMPT BUILDER (Now includes distance, transport, profit)
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

    # Format markets with deeper insight (distance, transport, profit)
    formatted = []
    for i, m in enumerate(markets, start=1):

        # fallback distance description if distance_km missing
        if "distance_km" in m:
            distance_text = f"{m['distance_km']} km away"
        else:
            distance_text = score_distance(county_clean, m["county"])

        transport_text = f"Transport: {m.get('transport_cost', 'N/A')} KES"
        profit_text = f"Effective Profit: {m.get('effective_profit', 'N/A')} KES"

        formatted.append(
            f"{i}. {m['market']} – Price: {m['retail_price']} KES, "
            f"{distance_text}, {transport_text}, {profit_text}"
        )

    markets_text = "\n".join(formatted)

    # Language toggles
    include_sw = (language == "sw" or language == "both")
    include_local = (language == "local" or language == "both")

    base = f"""
You are an agricultural assistant helping a Kenyan farmer to decide the best market to sell produce.

Address the farmer directly by name throughout the explanation.

FARMER DETAILS:
- Name: {name}
- County: {county_clean}
- Crop: {crop_clean}

Below are the ONLY 3 markets pre-selected by the system. 
Each has: price, estimated distance, transport cost, and effective profit.
{markets_text}

YOUR TASK:
1. Speak directly to {name}, e.g. "**{name}**, the nearest and most profitable market for you is..."
2. Choose **ONE best market**, using:
   - Highest effective profit
   - Lower transport cost
   - General proximity (distance_km)
3. Explain why in **2–3 simple English sentences**.
4. Give a **one-sentence comparison** for the remaining two markets.
5. Provide advice on:
   - The best time to sell (e.g., mornings, market days)
   - How transport cost affects profit
   - How to minimize cost (shared transport, early departures)
6. Do NOT create new markets or new data. Stay ONLY within the given values.

PRIMARY LANGUAGE:
Your main explanation MUST be in English.

"""

    if include_sw:
        base += f"""
OPTIONAL SWAHILI VERSION:
After the English explanation, provide a short Swahili summary (2–3 sentences),
addressing the farmer by name and using the same ranking.
"""

    if include_local:
        dialect = "a culturally appropriate local dialect for the farmer's county"
        base += f"""
OPTIONAL LOCAL DIALECT:
Provide ONE respectful sentence in {dialect}, summarizing the recommendation.
"""

    base += """
WHATSAPP FORMATTING RULES:
- Use clean line breaks.
- You MAY use:
    • Bullet points (•)
    • Bold text using **John** style
- Keep the explanation compact and actionable.
"""

    return base.strip()


# -----------------------------------------------------------
# GEMINI REQUEST HANDLER
# -----------------------------------------------------------
async def generate_explanation(
    farmer_name: Optional[str],
    county: str,
    crop: str,
    markets: List[Dict],
    language: str = "en"
) -> str:

    if not markets:
        return f"{farmer_name or 'Mkulima'}, hakuna masoko yanayopatikana kwa {crop} katika eneo ulilotaja."

    if not GEMINI_API_KEY:
        best = markets[0]
        return (
            f"{farmer_name}, based on available data, the best market is {best['market']} "
            f"with a price of {best['retail_price']} KES. Please consider transport cost."
        )

    # Build expanded prompt
    prompt = build_prompt(farmer_name, county, crop, markets, language)

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    # Send request
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(GEMINI_URL, headers=headers, json=payload)
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
            "Kindly account for distance and transport before making a decision."
        )
