from django.views import View
from django.http import JsonResponse
from source.services.stock import StockService
from source.serializers.serializer import Serializer
from source.serializers.stocks import StocksSerializer
from source.services.dashboard import DashboardService

class DashboardPeriodsView(View):
    def get(self, request, stock):
        service = DashboardService()
        rows = service.get_all_periods_from_stock(stock)
        serializer = Serializer(rows)
        return JsonResponse(serializer.data, safe=False)