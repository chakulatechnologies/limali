import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from datetime import datetime

from markets.models import Market
from prices.models import MarketPrice


class CSVUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        csv_file = request.FILES.get("file")

        if not csv_file:
            return Response({"error": "CSV file is required"}, status=400)

        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            return Response({"error": f"Could not read CSV: {str(e)}"}, status=400)

        # Normalize headers: lowercase + strip spaces
        df.columns = df.columns.str.strip().str.lower()

        # DEBUG
        print("Incoming Columns:", df.columns.tolist())

        # Required mapping
        rename_map = {
            "county": "county",
            "market": "market",
            "crop": "crop",
            "wholesale_price_kes": "wholesale_price",
            "retail_price_kes": "retail_price",
        }

        # Rename known fields
        df = df.rename(columns=rename_map)

        # System-generated date
        df["date"] = datetime.today().strftime("%Y-%m-%d")

        required_cols = ["county", "market", "crop", "wholesale_price", "retail_price", "date"]

        # Check required columns
        for col in required_cols:
            if col not in df.columns:
                return Response({"error": f"Missing required column: {col}"}, status=400)

        # Process rows
        created_markets = 0
        created_prices = 0

        for _, row in df.iterrows():
            market_obj, created = Market.objects.get_or_create(
                name=row["market"],
                defaults={
                    "county": row["county"],
                    "latitude": 0.0,
                    "longitude": 0.0,
                }
            )
            if created:
                created_markets += 1

            MarketPrice.objects.create(
                date=row["date"],
                crop=row["crop"],
                market=market_obj,
                wholesale_price=row["wholesale_price"],
                retail_price=row["retail_price"],
            )
            created_prices += 1

        return Response({
            "message": "CSV processed successfully",
            "markets_created": created_markets,
            "prices_records_added": created_prices
        })
