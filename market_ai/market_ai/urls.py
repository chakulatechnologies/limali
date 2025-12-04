from django.contrib import admin
from django.urls import path
from forecasting.views import MarketForecastView
from ai.views import MarketAdviceView
from recommendations.views import MarketRecommendationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/market/forecast/', MarketForecastView.as_view()),
    path("api/market/advice/", MarketAdviceView.as_view()),
    path('api/market/recommend/', MarketRecommendationView.as_view()),

]
