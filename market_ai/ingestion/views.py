import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from prices.models import MarketPrice, Market

class UploadMarketCSV(APIView):

    def post(self, request):
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response({"error": "No file provided"}, status=400)

        # Save temporarily
        file_path = default_storage.save(f"data/raw/{csv_file.name}", csv_file)

        df = pd.read_csv(file_path)

        required_cols = ['date', 'county', 'market', 'crop', 'retail_price', 'wholesale_price']
        if not all(col in df.columns for col in required_cols):
            return Response({"error": "CSV missing required columns"}, status=400)

        for _, row in df.iterrows():
            market_obj, _ = Market.objects.get_or_create(
                name=row['market'],
                county=row['county']
            )

            MarketPrice.objects.update_or_create(
                market=market_obj,
                crop=row['crop'].lower(),
                date=row['date'],
                defaults={
                    'retail_price': row['retail_price'],
                    'wholesale_price': row['wholesale_price']
                }
            )

        return Response({"message": "CSV processed successfully"}, status=200)
