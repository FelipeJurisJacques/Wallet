from django.db import models
from .historic import HistoricModel

class PeriodModel(models.Model):
    id = models.AutoField(primary_key=True)
    period = models.IntegerField(db_index=True)
    historical = models.ManyToManyField(HistoricModel, on_delete=models.CASCADE, db_index=True)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'periods'

