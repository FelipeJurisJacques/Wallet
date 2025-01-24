from django.views import View
from django.http import JsonResponse
from source.services.api.analyze import Analyze
from source.serializers.serializer import Serializer

class Analyzes(View):
    def get(self, request, stock):
        service = Analyze()
        return JsonResponse({
            'analyzes': Serializer.encode(
                service.get_all_from_stock(stock)
            ),
        }, safe=False)