from django.views import View
from django.http import Http404
from django.http import JsonResponse
from source.entities.stock import Stock
from source.services.historic import Historic as HistoricService
from source.serializers.historical import Historical as Serializer

class Historical(View):
    def get(self, request, stock):
        entity = Stock.find(stock)
        if entity is None:
            raise Http404('stock not found')
        service = HistoricService()
        entities = service.get_all_from_stock(entity)
        serializer = Serializer(entities)
        return JsonResponse(serializer.data, safe=False)