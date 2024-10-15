from django.views import View
from django.http import Http404
from django.http import JsonResponse
from source.models.stock import StockModel
from source.services.historical import HistoricalService
from source.serializers.historical import HistoricalSerializer

class HistoricalView(View):
    def get(self, request, stock):
        model = StockModel.find(stock)
        if model is None:
            raise Http404('stock not found')
        service = HistoricalService()
        entities = service.get_all_from_stock(model)
        serializer = HistoricalSerializer(entities)
        return JsonResponse(serializer.data, safe=False)