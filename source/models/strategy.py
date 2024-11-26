from django.db import models
from .period import ProphesyPeriodModel

class StrategyModel(models.Model):
    id = models.AutoField(primary_key=True)
    period = models.OneToOneField(ProphesyPeriodModel, on_delete=models.CASCADE, db_index=True)
    qualitative = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    quantitative = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'strategies'