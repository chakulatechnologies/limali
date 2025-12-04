from django.db import models
from forecasting.models import ForecastResult

class AIAuditLog(models.Model):
    forecast = models.ForeignKey(ForecastResult, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=255)
    data_sources = models.JSONField()
    prompt_snippet = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
