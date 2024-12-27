from datetime import datetime
from django.views import View
from django.http import JsonResponse
from source.serializers.serializer import Serializer
from source.services.dashboard import DashboardService

class DashboardHistoricalView(View):
    def get(self, request):
        if request.GET.get('StockId') is None:
            return JsonResponse({'error': 'StockId is required'}, status=400)
        if request.GET.get('StartDate') is None:
            return JsonResponse({'error': 'StartDate is required'}, status=400)
        service = DashboardService()
        end = None
        if request.GET.get('EndDate') is None:
            end = datetime.now()
        else:
            end = datetime.fromisoformat(request.GET.get('EndDate'))
        rows = service.get_historical(
            request.GET.get('StockId'),
            datetime.fromisoformat(request.GET.get('StartDate')),
            end,
        )
        serializer = Serializer(rows)
        return JsonResponse(serializer.data, safe=False)