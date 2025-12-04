import os
import joblib
import pandas as pd
from prophet.serialize import model_to_json, model_from_json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ForecastRequestSerializer
from markets.models import Market
from prices.models import MarketPrice

MODEL_DIR = "models/prophet/"


class MarketForecastView(APIView):

    def post(self, request):
        serializer = ForecastRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        crop = serializer.validated_data["crop"].lower()
        county = serializer.validated_data["county"]
        days = serializer.validated_data["days"]

        # 1. Find markets in that county
        markets = Market.objects.filter(county__iexact=county)
        if not markets.exists():
            return Response({"error": "No markets found in this county"}, status=404)

        results = []

        for market in markets:
            model_path = f"{MODEL_DIR}/{crop}_{market.name.replace(' ', '_')}.pkl"

            if not os.path.exists(model_path):
                # Model not trained for this market×crop
                continue

            try:
                model = joblib.load(model_path)
            except Exception:
                continue

            # Build future dataframe for Prophet
            future = model.make_future_dataframe(periods=days)
            forecast = model.predict(future)

            # Extract only the future values (last N days)
            forecast_tail = forecast.tail(days)[["ds", "yhat"]]

            predictions = [
                {"date": str(row["ds"].date()), "price": float(row["yhat"])}
                for _, row in forecast_tail.iterrows()
            ]

            results.append({
                "market": market.name,
                "county": market.county,
                "predictions": predictions
            })

        if not results:
            return Response({"error": "No trained models found for this crop in this county"}, status=404)

        response_data = {
            "crop": crop,
            "forecasts": results
        }

        return Response(response_data, status=200)
