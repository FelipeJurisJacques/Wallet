from django.db import models
from .stock import StockModel
from .historic_day import HistoricDayModel
from .prophesy_day import ProphesyDayModel

class StrategyDayModel(models.Model):
    id = models.AutoField(primary_key=True)
    historic_id = models.ForeignKey(HistoricDayModel, on_delete=models.CASCADE)
    qualitative = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantitative = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'strategy_day'