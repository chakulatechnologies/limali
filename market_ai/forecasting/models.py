from django.db import models
from users.models import UserProfile

class ForecastResult(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    crop = models.CharField(max_length=50)
    best_market = models.CharField(max_length=100)
    best_sell_start = models.DateField()
    best_sell_end = models.DateField()
    confidence = models.CharField(max_length=20)
    explanation = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
