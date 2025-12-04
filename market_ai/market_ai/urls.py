from django.contrib import admin
from django.urls import path, include
from forecasting.views import MarketForecastView
from ai.views import MarketAdviceView
from recommendations.views import MarketRecommendationView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include ingestion routes FIRST
    path('api/market/', include('ingestion.urls')),

    # Other specific routes
    path('api/market/forecast/', MarketForecastView.as_view()),
    path("api/market/advice/", MarketAdviceView.as_view()),
    path('api/market/recommend/', MarketRecommendationView.as_view()),
]
