from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from recommendations.views import MarketRecommendationView
from ai.services import generate_explanation, save_ai_audit
from forecasting.models import ForecastResult


class MarketAdviceView(APIView):

    def post(self, request):
        crop = request.data.get("crop")
        county = request.data.get("county")
        lat = request.data.get("lat")
        lon = request.data.get("lon")

        if not crop or not county:
            return Response({"error": "crop and county are required"}, status=400)

        # STEP 1 — Get recommendation results (reuse Step 3)
        recommendation_view = MarketRecommendationView()
        rec_response = recommendation_view.post(request).data

        if "error" in rec_response:
            return Response(rec_response, status=400)

        ranked = rec_response["recommendations"]
        best_market = rec_response["best_market"]

        # STEP 2 — Build AI context JSON
        context = {
            "crop": crop,
            "county": county,
            "best_market": best_market,
            "rankings": ranked,
            "farmer_location": {"lat": lat, "lon": lon},
            "data_sources": [
                "Market CSV (wholesale & retail)",
                "Prophet forecast",
                "Distance-based transport cost"
            ]
        }

        # STEP 3 — Generate AI explanation
        explanation = generate_explanation(context)

        # STEP 4 — Save forecast result
        forecast_result = ForecastResult.objects.create(
            user=None,  # attach real user later
            crop=crop,
            best_market=best_market["market"],
            best_sell_start=best_market["best_sell_start"],
            best_sell_end=best_market["best_sell_end"],
            confidence="medium",
            explanation=explanation
        )

        # STEP 5 — Audit log
        save_ai_audit(forecast_result, context, explanation)

        # STEP 6 — Final response
        return Response({
            "crop": crop,
            "county": county,
            "best_market": best_market,
            "recommendations": ranked,
            "advice": explanation
        }, status=200)
