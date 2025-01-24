from django.urls import path
from ..views.api.stocks import Stocks
from ..views.api.analyzes import Analyzes
from ..views.api.timelines import Timelines
from ..views.api.historical import Historical
# from ..views.api.prophesy import ProphesyView
# from ..views.api.dashboard_periods import DashboardPeriodsView
# from ..views.api.dashboard_prophesied import DashboardProphesiedView
# from ..views.api.dashboard_historical import DashboardHistoricalView

urlpatterns = [
     path('stocks/', Stocks.as_view()),
     path('timeline/', Timelines.as_view()),
     path('analyzes/<int:stock>/', Analyzes.as_view()),
     path('historical/<int:stock>/', Historical.as_view()),
#     path('prophesy/<int:stock>/', ProphesyView.as_view()),
#     path('dashboard/prophesy/', DashboardProphesiedView.as_view()),
#     path('dashboard/historic/', DashboardHistoricalView.as_view()),
]
