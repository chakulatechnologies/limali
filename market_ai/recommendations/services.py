import math
import pandas as pd

TRANSPORT_COST_PER_KM = 20  # can be configured later


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two lat/lon points.
    Returns distance in kilometers.
    """
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    return R * (2 * math.asin(math.sqrt(a)))


def compute_effective_profit(predicted_price, distance_km):
    transport_cost = distance_km * TRANSPORT_COST_PER_KM
    return predicted_price - transport_cost


def find_best_selling_window(predictions_df, top_percent=0.15):
    """
    Given a forecast dataframe (date, price), return the best window.
    Takes top 15% of forecasted prices and clusters into a start→end window.
    """

    # convert to DataFrame
    df = pd.DataFrame(predictions_df)
    
    # Find price threshold (top X%)
    threshold = df["price"].quantile(1 - top_percent)

    # Filter rows above that threshold
    df_high = df[df["price"] >= threshold]

    if df_high.empty:
        # fallback: use the day with highest price
        max_row = df.loc[df["price"].idxmax()]
        return str(max_row["date"]), str(max_row["date"])

    # Start and end of selling window
    start = df_high["date"].min()
    end = df_high["date"].max()

    return str(start), str(end)


def rank_markets(forecast_results, user_lat, user_lon):
    """
    Main recommendation function:
    Input:
      forecast_results: [
        {
          "market": "Nairobi",
          "lat": -1.2833,
          "lon": 36.8167,
          "predictions": [ {date, price}, ... ]
        }
      ]
      user_lat, user_lon -> farmer location

    Output:
      Ranked list with effective profit & selling window
    """

    ranked = []

    for item in forecast_results:
        market_name = item["market"]
        market_lat = item.get("lat")
        market_lon = item.get("lon")

        # Compute distance if coordinates exist
        distance_km = None
        if market_lat and market_lon and user_lat and user_lon:
            distance_km = haversine_distance(user_lat, user_lon, market_lat, market_lon)
        else:
            distance_km = 10  # fallback if lat/lon missing

        # Convert predictions to df
        df = pd.DataFrame(item["predictions"])
        avg_price = df["price"].mean()
        max_price = df["price"].max()

        # Effective profit
        effective_profit = compute_effective_profit(max_price, distance_km)

        # Best selling window
        start, end = find_best_selling_window(df)

        ranked.append({
            "market": market_name,
            "distance_km": round(distance_km, 2),
            "avg_price": round(avg_price, 2),
            "max_price": round(max_price, 2),
            "effective_profit": round(effective_profit, 2),
            "best_sell_start": start,
            "best_sell_end": end
        })

    # Rank by effective profit
    ranked_sorted = sorted(ranked, key=lambda x: x["effective_profit"], reverse=True)

    return ranked_sorted
