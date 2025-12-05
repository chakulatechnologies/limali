# profit_forecast.py
import pandas as pd

def forecast_profit_trend(df: pd.DataFrame, crop: str, market_name: str):
    """
    Very lightweight trend analysis.
    Looks for price patterns within the CSV (simulated trend).
    """

    # Filter data for the specific market + crop
    sub = df[
        (df["market"].str.lower() == market_name.lower())
        & (df["crop_norm"] == crop.lower())
    ]

    if len(sub) < 2:
        return {
            "trend": "unknown",
            "message": "No price history available to determine trend."
        }

    # Using retail price trend
    prices = sub["retail_price"].tolist()

    if prices[-1] > prices[-2]:
        return {
            "trend": "rising",
            "message": f"Prices at {market_name} appear to be rising. Selling early may secure a better price."
        }
    elif prices[-1] < prices[-2]:
        return {
            "trend": "falling",
            "message": f"Prices at {market_name} have been falling recently. You may need to negotiate strongly or consider alternative markets."
        }
    else:
        return {
            "trend": "stable",
            "message": f"Prices at {market_name} are stable. Selling anytime today or tomorrow should give similar outcomes."
        }
