from django.db import models

class Market(models.Model):
    name = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.county})"
