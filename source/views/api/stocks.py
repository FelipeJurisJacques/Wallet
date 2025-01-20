from django.views import View
from django.http import JsonResponse
from source.entities.stock import Stock
from source.serializers.stocks import Stocks as Serializer

class Stocks(View):
    def get(self, request):
        entities = Stock.all()
        serializer = Serializer(entities)
        return JsonResponse(serializer.data, safe=False)