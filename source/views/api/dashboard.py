from django.views import View
from django.http import JsonResponse
from source.services.stock import StockService
from source.serializers.serializer import Serializer
from source.services.prophesy import ProphesyService

class DashboardView(View):
    def get(self, request):
        stock_service = StockService()
        prophesy_service = ProphesyService()
        stocks = stock_service.all()
        for stock in stocks:
            prophesied = prophesy_service.get_all_from_stock(stock)
            serializer = Serializer(prophesied)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse({}, safe=False)