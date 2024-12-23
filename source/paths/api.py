from django.urls import path
from ..views.api.stocks import StocksView
from ..views.api.prophesy import ProphesyView
from ..views.api.historical import HistoricalView
from ..views.api.dashboard_periods import DashboardPeriodsView
from ..views.api.dashboard_prophesy import DashboardProphesyView

urlpatterns = [
    path('stocks/', StocksView.as_view()),
    path('prophesy/<int:stock>/', ProphesyView.as_view()),
    path('historical/<int:stock>/', HistoricalView.as_view()),
    path('dashboard/periods/<int:stock>/', DashboardPeriodsView.as_view()),
    path('dashboard/prophesy/<int:period>/', DashboardProphesyView.as_view()),
]
