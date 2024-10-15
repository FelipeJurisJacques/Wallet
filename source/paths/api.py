from django.urls import path
from source.views.api.stocks import StocksView
from source.views.api.historical import HistoricalView

urlpatterns = [
    path('stocks/', StocksView.as_view()),
    path('historical/<int:stock>/', HistoricalView.as_view()),
]
