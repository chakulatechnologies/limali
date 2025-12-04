from rest_framework import serializers

class ForecastRequestSerializer(serializers.Serializer):
    crop = serializers.CharField()
    county = serializers.CharField()
    days = serializers.IntegerField(default=30)
