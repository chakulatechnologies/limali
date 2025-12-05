# profit_model.py

import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# -----------------------------------------------------------
# 1️⃣ County-center coordinates (approximate)
# -----------------------------------------------------------
COUNTY_COORDS = {
    "uasin gishu": (-0.5143, 35.2698),
    "nakuru": (-0.3031, 36.0800),
    "kisumu": (-0.0917, 34.7679),
    "bungoma": (0.5690, 34.5584),
    "nairobi": (-1.2864, 36.8172),
    "kajiado": (-1.8537, 36.7763),
    "kiambu": (-1.0397, 37.0825),
    "kericho": (-0.3689, 35.2833),
    "nyeri": (-0.4197, 36.9473),
    "meru": (0.3557, 37.8088),
    "mombasa": (-4.0435, 39.6682),
    "makueni": (-1.8032, 37.6200),
    "machakos": (-1.5167, 37.2667),
    "kisii": (-0.6773, 34.7796),
    "siaya": (0.0607, 34.2881),
    # Add more counties as needed
}

# -----------------------------------------------------------
# 2️⃣ Region clusters (same as before)
# -----------------------------------------------------------
REGION_CLUSTERS = {
    "nairobi_metropolitan": {
        "counties": ["nairobi", "kajiado", "kiambu", "machakos"]
    },
    "rift_valley": {
        "counties": ["nakuru", "uasin gishu", "kericho", "baringo", "bomet", "laikipia"]
    },
    "western": {
        "counties": ["kakamega", "vihiga", "bungoma", "busia"]
    },
    "nyanza": {
        "counties": ["kisumu", "homa bay", "migori", "siaya", "kisii", "nyamira"]
    },
    "central": {
        "counties": ["nyeri", "kirinyaga", "murang'a", "muranga", "embu"]
    },
    "coast": {
        "counties": ["mombasa", "kilifi", "lamu", "kwale", "taita taveta"]
    },
    "eastern": {
        "counties": ["meru", "kitui", "makueni", "tharaka nithi"]
    }
}

# -----------------------------------------------------------
# 3️⃣ Determine region
# -----------------------------------------------------------
def get_region(county: str):
    county_clean = county.lower().strip()
    for region, data in REGION_CLUSTERS.items():
        if county_clean in data["counties"]:
            return region
    return None

# -----------------------------------------------------------
# 4️⃣ Haversine Distance (km)
# -----------------------------------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2)**2 +
        cos(radians(lat1)) * cos(radians(lat2)) *
        sin(dlon / 2)**2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# -----------------------------------------------------------
# 5️⃣ Main Ranking Logic (now includes distance)
# -----------------------------------------------------------
def compute_top_markets(df: pd.DataFrame, farmer_location: str, crop: str):

    crop_clean = crop.lower().strip()
    farmer_region = get_region(farmer_location)

    # Normalize search term
    farmer_key = farmer_location.lower().strip()

    # Get farmer coords
    farmer_coords = COUNTY_COORDS.get(farmer_key)
    if not farmer_coords:
        # fallback = Nairobi center
        farmer_coords = COUNTY_COORDS["nairobi"]

    farmer_lat, farmer_lon = farmer_coords

    # Filter crop
    df_crop = df[df["crop_norm"] == crop_clean].copy()
    if df_crop.empty:
        return []

    # Region flag
    if farmer_region:
        df_crop["in_farmer_region"] = df_crop["county_norm"].apply(
            lambda x: 1 if x in REGION_CLUSTERS[farmer_region]["counties"] else 0
        )
    else:
        df_crop["in_farmer_region"] = 0

    # Compute county-center distances
    distances = []
    for _, row in df_crop.iterrows():
        county = row["county_norm"]
        coords = COUNTY_COORDS.get(county)

        if not coords:
            distances.append(None)
        else:
            dist = haversine(farmer_lat, farmer_lon, coords[0], coords[1])
            distances.append(round(dist, 2))

    df_crop["distance_km"] = distances

    # Profit = price only (since no transport model)
    df_crop["effective_profit"] = df_crop["retail_price"]

    # Median price stability filter
    median_price = df_crop["retail_price"].median()
    df_crop["median_diff"] = abs(df_crop["retail_price"] - median_price)

    # Final sort:
    df_ranked = df_crop.sort_values(
        by=["in_farmer_region", "retail_price", "median_diff"],
        ascending=[False, False, True]
    )

    # Pick top 3
    top3 = df_ranked.head(3)

    return [
        {
            "market": row["market"],
            "county": row["county"],
            "retail_price": row["retail_price"],
            "distance_km": row["distance_km"],
            "effective_profit": row["effective_profit"]
        }
        for _, row in top3.iterrows()
    ]
