from django.contrib import admin
from .models.stock import StockModel
from .models.historic import HistoricModel
from .models.prophesy import ProphesyModel

admin.site.register(StockModel)
admin.site.register(HistoricModel)
admin.site.register(ProphesyModel)
