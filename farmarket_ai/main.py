# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

from profit_model import compute_top_markets
from gemini_client import generate_explanation


class FarmerRequest(BaseModel):
    name: str | None = None
    county: str
    crop: str


class AdviceResponse(BaseModel):
    best_markets: list
    explanation: str


app = FastAPI(title="FarmSmart AI")


@app.on_event("startup")
def load_csv():
    global df
    try:
        # Load CSV
        df = pd.read_csv("markets.csv")

        # Rename the CSV headers to what the model expects
        df = df.rename(columns={
            "County": "county",
            "Market": "market",
            "Crop": "crop",
            "Retail_Price_KES": "retail_price"
        })

        # Note: "Unit" column stays in the DataFrame but is ignored by the model
        print(f"Loaded {len(df)} market rows with corrected column names.")

    except Exception as e:
        raise RuntimeError(f"Cannot load CSV: {e}")


@app.post("/advise", response_model=AdviceResponse)
async def advise(payload: FarmerRequest):
    top_markets = compute_top_markets(df, payload.county, payload.crop)

    if not top_markets:
        raise HTTPException(
            404, "Hakuna data ya soko inayolingana na mazao haya."
        )

    explanation = await generate_explanation(
        payload.name, payload.county, payload.crop, top_markets
    )

    return AdviceResponse(best_markets=top_markets, explanation=explanation)
