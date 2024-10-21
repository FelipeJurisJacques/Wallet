from django.contrib import admin
from .models.stock import StockModel
from .models.historic_day import HistoricDayModel
from .models.prophesy_day import ProphesyDayModel
from .models.prophesy_forecast_day import ProphesyForecastDayModel

admin.site.register(StockModel)
admin.site.register(HistoricDayModel)
admin.site.register(ProphesyDayModel)
admin.site.register(ProphesyForecastDayModel)