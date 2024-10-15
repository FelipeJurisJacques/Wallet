from django.views import View
from django.http import JsonResponse
from source.services.stock import StockService
from source.serializers.stocks import StocksSerializer

class StocksView(View):
    def get(self, request):
        service = StockService()
        entities = service.all()
        serializer = StocksSerializer(entities)
        return JsonResponse(serializer.data, safe=False)