import os
import django
import pandas as pd
from prophet import Prophet
import joblib
from datetime import datetime

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "market_ai.settings")
django.setup()

from prices.models import MarketPrice, Market

# Directory to save Prophet models
MODEL_DIR = "models/prophet/"

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)


def get_market_crop_pairs():
    """
    Fetch all unique (crop, market) combinations from DB.
    """
    qs = MarketPrice.objects.values_list("crop", "market__name", "market__county").distinct()
    pairs = [(crop, market, county) for crop, market, county in qs]
    return pairs


def load_price_dataframe(crop, market_name):
    """
    Load price series for a given crop and market.
    Returns cleaned pandas DataFrame in (ds, y) format for Prophet.
    """
    qs = MarketPrice.objects.filter(
        crop=crop,
        market__name=market_name
    ).order_by("date")

    if not qs.exists():
        return None

    df = pd.DataFrame(list(qs.values("date", "retail_price", "wholesale_price")))

    # Prefer wholesale price if available, else retail
    df["price"] = df["wholesale_price"].fillna(df["retail_price"])

    # Clean missing data
    df = df.dropna(subset=["price"])

    if df.empty:
        return None

    df.rename(columns={"date": "ds", "price": "y"}, inplace=True)

    # Prophet requires datetime
    df["ds"] = pd.to_datetime(df["ds"])

    return df[["ds", "y"]]


def train_prophet_for_pair(crop, market_name, county):
    """
    Train a Prophet model for a specific crop×market combination.
    """
    df = load_price_dataframe(crop, market_name)
    if df is None or len(df) < 10:  # Minimum data
        print(f"Skipping {crop} × {market_name}: Not enough data")
        return

    print(f"Training Prophet model for {crop} × {market_name}")

    model = Prophet(
        seasonality_mode="additive",
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(df)

    # Save model to disk
    filename = f"{MODEL_DIR}/{crop}_{market_name.replace(' ', '_')}.pkl"
    joblib.dump(model, filename)

    print(f"Saved model → {filename}")


def main():
    print("=== Prophet Training Started ===")
    print(f"Time: {datetime.now()}")

    pairs = get_market_crop_pairs()

    print(f"Found {len(pairs)} crop×market combinations")

    for crop, market_name, county in pairs:
        train_prophet_for_pair(crop, market_name, county)

    print("=== Training Completed Successfully ===")


if __name__ == "__main__":
    main()
