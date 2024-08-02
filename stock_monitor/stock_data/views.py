from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import DailyStock
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.db.models import Max, Min, F, ExpressionWrapper, FloatField


# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.forms import AuthenticationForm
# from .forms import UserRegisterForm


def daily_closing_price(request):
    stocks = DailyStock.objects.all().values('symbol', 'date', 'close')
    return JsonResponse(list(stocks), safe=False)


# def price_change_percentage(request):
#     periods = {
#         '24h': timedelta(days=1),
#         '30d': timedelta(days=30),
#         '1y': timedelta(days=365),
#     }
#     results = {}
#     today = datetime.now().date()

#     for period, delta in periods.items():
#         start_date = today - delta
#         stocks = DailyStock.objects.filter(date__gte=start_date).values('symbol').annotate(
#             start_price=Min('open'),
#             end_price=Max('close')
#         ).annotate(
#             percentage_change=ExpressionWrapper(
#                 (F('end_price') - F('start_price')) / F('start_price') * 100,
#                 output_field=FloatField()
#             )
#         ).values('symbol', 'percentage_change')
        
#         results[period] = list(stocks)




def price_change_percentage(request):
    periods = {
        '24h': timedelta(days=1),
        '30d': timedelta(days=30),
        '1y': timedelta(days=365),
    }
    results = {}
    today = datetime.now().date()

    for period, delta in periods.items():
        start_date = today - delta
        stocks = DailyStock.objects.filter(date__gte=start_date).values('symbol').annotate(
            start_price=Min('open'),
            end_price=Max('close'),
            current_price=Max('close'),  # Latest close price
            start_date=Min('date'),
            end_date=Max('date')
        ).annotate(
            percentage_change=ExpressionWrapper(
                (F('end_price') - F('start_price')) / F('start_price') * 100,
                output_field=FloatField()
            )
        ).values('symbol', 'percentage_change', 'current_price', 'start_date', 'end_date')
        
        results[period] = list(stocks)
    
    return JsonResponse(results)




    return JsonResponse(results)

def top_gainers_losers(request):
    today = datetime.now().date()
    start_date = today - timedelta(days=1)

    stock_changes = DailyStock.objects.filter(date__range=[start_date, today]).values('symbol').annotate(
        start_price=Min('open'),
        end_price=Max('close')
    ).annotate(
        percentage_change=ExpressionWrapper(
            (F('end_price') - F('start_price')) / F('start_price') * 100,
            output_field=FloatField()
        )
    ).order_by('-percentage_change')

    top_gainers = stock_changes[:10]
    top_losers = stock_changes[::-1][:10]

    return JsonResponse({
        'top_gainers': list(top_gainers),
        'top_losers': list(top_losers)
    })



