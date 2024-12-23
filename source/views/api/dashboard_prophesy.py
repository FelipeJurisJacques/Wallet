from django.views import View
from django.http import JsonResponse
from source.serializers.serializer import Serializer
from source.services.dashboard import DashboardService

class DashboardProphesyView(View):
    def get(self, request, period):
        service = DashboardService()
        rows = service.get_period_prophesied(period)
        serializer = Serializer(rows)
        return JsonResponse(serializer.data, safe=False)