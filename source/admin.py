from django.contrib import admin
from .models.stock import Stock
from .models.analyze import Analyze
from .models.forecast import Forecast
from .models.historic import Historic
from .models.prophesy import Prophesy
from .models.timeline import Timeline

admin.site.register(Stock)
admin.site.register(Analyze)
admin.site.register(Forecast)
admin.site.register(Historic)
admin.site.register(Prophesy)
admin.site.register(Timeline)