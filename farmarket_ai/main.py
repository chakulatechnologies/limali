# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

from profit_model import compute_top_markets
from gemini_client import generate_explanation
from profit_tips import transport_savings_tips
from profit_forecast import forecast_profit_trend


# -----------------------------------------------
# REQUEST MODEL
# -----------------------------------------------
class FarmerRequest(BaseModel):
    name: str | None = None
    county: str
    crop: str
    language: str | None = "en"   # "en" | "sw" | "local" | "both"


# -----------------------------------------------
# RESPONSE MODEL
# -----------------------------------------------
class AdviceResponse(BaseModel):
    best_markets: list
    explanation: str


app = FastAPI(title="FarmSmart AI")


# -----------------------------------------------
# LOAD CSV + NORMALIZE FIELDS
# -----------------------------------------------
@app.on_event("startup")
def load_csv():
    global df
    try:
        df = pd.read_csv("markets.csv")

        # Standardize expected headers
        df = df.rename(columns={
            "County": "county",
            "Market": "market",
            "Crop": "crop",
            "Retail_Price_KES": "retail_price"
        })

        # Normalized filter keys
        df["crop_norm"] = df["crop"].str.lower().str.strip()
        df["county_norm"] = df["county"].str.lower().str.strip()
        df["market_norm"] = df["market"].str.lower().str.strip()

        print(f"Loaded {len(df)} market rows with normalized fields.")

    except Exception as e:
        raise RuntimeError(f"Cannot load CSV: {e}")


# -----------------------------------------------
# ADVISE ENDPOINT
# -----------------------------------------------
@app.post("/advise", response_model=AdviceResponse)
async def advise(payload: FarmerRequest):

    # Try to compute best markets
    top_markets = compute_top_markets(df, payload.county, payload.crop)

    # ----------------------------------------------------
    # NEW LOGIC: Soft fallback when no market matches
    # ----------------------------------------------------
    if not top_markets:
        explanation = await generate_explanation(
            farmer_name=payload.name,
            county=payload.county,
            crop=payload.crop,
            markets=[],                    # empty → Gemini general advice
            language=payload.language
        )

        # We return empty best_markets but meaningful Gemini advice
        return AdviceResponse(best_markets=[], explanation=explanation)

    # ----------------------------------------------------
    # Normal case: Enhance markets with trend + tips
    # ----------------------------------------------------
    for market in top_markets:
        trend = forecast_profit_trend(df, payload.crop, market["market"])
        market["trend_message"] = trend["message"]

        tips = transport_savings_tips(
            market.get("distance_km"), market.get("transport_cost")
        )
        market["tips"] = tips

    # Generate English + optional Swahili/local output
    explanation = await generate_explanation(
        farmer_name=payload.name,
        county=payload.county,
        crop=payload.crop,
        markets=top_markets,
        language=payload.language
    )

    # Return structured response
    return AdviceResponse(
        best_markets=top_markets,
        explanation=explanation
    )
