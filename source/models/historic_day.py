from django.db import models
from .stock import StockModel

class HistoricDayModel(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.IntegerField(db_index=True)
    stock = models.ForeignKey(StockModel, on_delete=models.CASCADE, db_index=True)
    open = models.DecimalField(max_digits=17, decimal_places=2)
    high = models.DecimalField(max_digits=17, decimal_places=2)
    low = models.DecimalField(max_digits=17, decimal_places=2)
    close = models.DecimalField(max_digits=17, decimal_places=2)
    volume = models.IntegerField()
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'historical_day'

