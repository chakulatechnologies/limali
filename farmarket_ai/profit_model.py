# profit_model.py

import pandas as pd
from math import radians, sin, cos, sqrt, atan2
from locations import TOWN_COORDINATES


# -------------------------------------------
# 1️⃣ Haversine Distance (km)
# -------------------------------------------
def compute_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius (km)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


# -------------------------------------------
# 2️⃣ Transport Cost Estimator (simple model)
#  - Assumes ~ KES 30 per km per standard load
# -------------------------------------------
def estimate_transport_cost(distance_km):
    return round(distance_km * 30)  # you can tune this later


# -------------------------------------------
# 3️⃣ Choose nearest market + best profit
# -------------------------------------------
def compute_top_markets(df: pd.DataFrame, farmer_location: str, crop: str):

    farmer_key = farmer_location.lower().strip()

    if farmer_key not in TOWN_COORDINATES:
        # fallback: treat county center as location
        user_lat, user_lon = TOWN_COORDINATES.get("kajiado", (None, None))
    else:
        user_lat, user_lon = TOWN_COORDINATES[farmer_key]

    # Normalize crop
    crop_clean = crop.lower().strip()

    # Filter dataset by crop
    df_crop = df[df["crop_norm"] == crop_clean].copy()

    if df_crop.empty:
        return []

    # Ensure coordinate columns exist
    if "lat" not in df_crop.columns or "lon" not in df_crop.columns:
        return []

    # Compute distance to each market
    df_crop["distance_km"] = df_crop.apply(
        lambda r: compute_distance(user_lat, user_lon, r["lat"], r["lon"]),
        axis=1
    )

    # Estimate transport cost
    df_crop["transport_cost"] = df_crop["distance_km"].apply(estimate_transport_cost)

    # Effective profit = price - transport
    df_crop["effective_profit"] = df_crop["retail_price"] - df_crop["transport_cost"]

    # Sort by best profit, then nearest
    df_sorted = df_crop.sort_values(
        by=["effective_profit", "distance_km"],
        ascending=[False, True]
    )

    # Return top 3
    top3 = df_sorted.head(3)

    return [
        {
            "market": row["market"],
            "county": row["county"],
            "retail_price": row["retail_price"],
            "distance_km": round(row["distance_km"], 2),
            "transport_cost": int(row["transport_cost"]),
            "effective_profit": int(row["effective_profit"])
        }
        for _, row in top3.iterrows()
    ]
