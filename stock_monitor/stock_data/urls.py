# stock_data/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('daily_closing_price/', views.daily_closing_price, name='daily_closing_price'),
    path('price_change_percentage/', views.price_change_percentage, name='price_change_percentage'),
    path('top_gainers_losers/', views.top_gainers_losers, name='top_gainers_losers'),
]
