from django.db import models
from users.models import UserProfile

class Farm(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    size_acres = models.FloatField(default=1.0)
    zone = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

class CropPlot(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    crop_type = models.CharField(max_length=50)
    area_acres = models.FloatField(default=1.0)
    planting_date = models.DateField(blank=True, null=True)
    yield_last_season = models.FloatField(blank=True, null=True)
    yield_unit = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
