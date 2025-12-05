# profit_model.py

import pandas as pd

# -----------------------------------------------------------
# 1️⃣ County / Region clusters (simple parent-area grouping)
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
# 2️⃣ Find which region a county belongs to
# -----------------------------------------------------------
def get_region(county: str):
    county_clean = county.lower().strip()
    for region, data in REGION_CLUSTERS.items():
        if county_clean in data["counties"]:
            return region
    return None


# -----------------------------------------------------------
# 3️⃣ Main Ranking Logic (No GPS, No Transport Cost)
# -----------------------------------------------------------
def compute_top_markets(df: pd.DataFrame, farmer_location: str, crop: str):

    crop_clean = crop.lower().strip()
    farmer_region = get_region(farmer_location)

    # Filter crops
    df_crop = df[df["crop_norm"] == crop_clean].copy()
    if df_crop.empty:
        return []

    # -------------------------------------------
    # If region known → prioritize markets in that region
    # -------------------------------------------
    if farmer_region:
        df_crop["in_farmer_region"] = df_crop["county_norm"].apply(
            lambda x: 1 if x in REGION_CLUSTERS[farmer_region]["counties"] else 0
        )
    else:
        df_crop["in_farmer_region"] = 0  # no region match fallback

    # -------------------------------------------
    # Compute median price for this crop
    # -------------------------------------------
    median_price = df_crop["retail_price"].median()

    # Distance from median (to avoid extreme markets)
    df_crop["median_diff"] = abs(df_crop["retail_price"] - median_price)

    # -------------------------------------------
    # Sort Priority:
    # 1. Markets in same region
    # 2. Highest retail price
    # 3. Closest to median price (stability)
    # -------------------------------------------
    df_ranked = df_crop.sort_values(
        by=["in_farmer_region", "retail_price", "median_diff"],
        ascending=[False, False, True]
    )

    # Return top 3
    top3 = df_ranked.head(3)

    return [
        {
            "market": row["market"],
            "county": row["county"],
            "retail_price": row["retail_price"],
            "in_farmer_region": int(row["in_farmer_region"]),
            "median_diff": float(row["median_diff"])
        }
        for _, row in top3.iterrows()
    ]
