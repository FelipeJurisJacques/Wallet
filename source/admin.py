from django.contrib import admin
from .models.stock import StockModel
from .models.period import PeriodModel
from .models.historic import HistoricModel
from .models.prophesy import ProphesyModel
from .models.forecast import ForecastModel
from .models.strategy import StrategyModel

admin.site.register(StockModel)
admin.site.register(PeriodModel)
admin.site.register(HistoricModel)
admin.site.register(ProphesyModel)
admin.site.register(ForecastModel)
admin.site.register(StrategyModel)