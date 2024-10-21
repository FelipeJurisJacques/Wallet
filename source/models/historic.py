from django.db import models
from .stock import StockModel

class HistoricModel(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(StockModel, on_delete=models.CASCADE)
    date = models.IntegerField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'historical'

