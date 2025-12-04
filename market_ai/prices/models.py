from django.db import models
from markets.models import Market

class MarketPrice(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    crop = models.CharField(max_length=50)
    date = models.DateField()
    retail_price = models.FloatField(blank=True, null=True)
    wholesale_price = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ('market', 'crop', 'date')
