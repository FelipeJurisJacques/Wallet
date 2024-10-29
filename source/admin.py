from django.contrib import admin
from .models.stock import StockModel
from .models.prophesy import ProphesyModel
from .models.historic_day import HistoricDayModel
from .models.prophesy_day import ProphesyDayModel
from .models.forecast_day import ForecastDayModel
from .models.strategy_day import StrategyDayModel

admin.site.register(StockModel)
admin.site.register(ProphesyModel)
admin.site.register(HistoricDayModel)
admin.site.register(ProphesyDayModel)
admin.site.register(ForecastDayModel)
admin.site.register(StrategyDayModel)