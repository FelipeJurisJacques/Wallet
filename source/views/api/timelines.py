from django.views import View
from django.http import JsonResponse
from source.services.api.timeline import Timeline
from source.serializers.serializer import Serializer

class Timelines(View):
    def get(self, request):
        if request.GET.get('AnalyzeId') is None:
            return JsonResponse({'error': 'AnalyzeId is required'}, status=400)
        service = Timeline()
        return JsonResponse({
            'timeline': Serializer.encode(
                service.get_all_from_analyze(request.GET.get('AnalyzeId'))
            ),
        }, safe=False)