from django.views import View
from django.http import JsonResponse
from source.services.stock import StockService
from source.serializers.stock import StockSerializer

class ApiView(View):
    def get(self, request):
        stock_service = StockService()
        stocks = stock_service.all()
        serializer = StockSerializer(stocks)
        return JsonResponse(serializer.data, safe=False)