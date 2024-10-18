from django.views import View
from django.http import Http404
from django.http import JsonResponse
from source.models.stock import StockModel
from source.serializers.serializer import Serializer
from source.services.prophesy import ProphesyService

class ProphesyView(View):
    def get(self, request, stock):
        model = StockModel.find(stock)
        if model is None:
            raise Http404('stock not found')
        service = ProphesyService()
        models = service.get_all_from_stock(model)
        serializer = Serializer(models)
        return JsonResponse({
            'prophesied': serializer.data,
        }, safe=False)