from django.db import models
from .historic_day import HistoricDayModel

class StrategyDayModel(models.Model):
    id = models.AutoField(primary_key=True)
    historic_id = models.ForeignKey(HistoricDayModel, on_delete=models.CASCADE)
    qualitative = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    quantitative = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'strategy_day'