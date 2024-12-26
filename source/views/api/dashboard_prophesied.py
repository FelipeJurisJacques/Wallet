from django.views import View
from django.http import JsonResponse
from source.serializers.serializer import Serializer
from source.services.dashboard import DashboardService

class DashboardProphesiedView(View):
    def get(self, request):
        if request.GET.get('PeriodId') is None:
            return JsonResponse({'error': 'PeriodId is required'}, status=400)
        service = DashboardService()
        rows = service.get_period_prophesied(request.GET.get('PeriodId'))
        serializer = Serializer(rows)
        return JsonResponse(serializer.data, safe=False)