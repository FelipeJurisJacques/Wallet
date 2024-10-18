from django.urls import path
from ..views.api.stocks import StocksView
from ..views.api.prophesy import ProphesyView
from ..views.api.dashboard import DashboardView
from ..views.api.historical import HistoricalView

urlpatterns = [
    path('stocks/', StocksView.as_view()),
    path('prophesy/<int:stock>/', ProphesyView.as_view()),
    path('dashboard/', DashboardView.as_view()),
    path('historical/<int:stock>/', HistoricalView.as_view()),
]
