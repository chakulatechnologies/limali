from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from markets.models import Market
from forecasting.views import MarketForecastView
from .services import rank_markets


class MarketRecommendationView(APIView):

    def post(self, request):
        crop = request.data.get("crop")
        county = request.data.get("county")
        user_lat = request.data.get("lat")
        user_lon = request.data.get("lon")
        days = request.data.get("days", 30)

        if not crop or not county:
            return Response({"error": "crop and county are required"}, status=400)

        # Step 1: Reuse forecast logic
        forecast_view = MarketForecastView()
        forecast_response = forecast_view.post(request).data

        if "error" in forecast_response:
            return Response(forecast_response, status=404)

        forecasts = forecast_response["forecasts"]

        # Attach lat/lon from Market model to each forecast row
        enhanced = []
        for item in forecasts:
            try:
                market_obj = Market.objects.get(name=item["market"])
                item["lat"] = market_obj.lat
                item["lon"] = market_obj.lon
            except:
                item["lat"] = None
                item["lon"] = None
            enhanced.append(item)

        # Step 2: Run ranking logic
        ranked_results = rank_markets(enhanced, user_lat, user_lon)

        # Step 3: Construct final response
        return Response({
            "crop": crop,
            "county": county,
            "recommendations": ranked_results,
            "best_market": ranked_results[0] if ranked_results else None
        }, status=200)
