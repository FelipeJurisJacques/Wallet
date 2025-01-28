from .stock import Stock
from django.db import models

class Timeline(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, db_index=True)
    working = models.IntegerField()
    datetime = models.IntegerField(db_index=True)

    class Meta:
        db_table = 'timelines'
        unique_together = ('type', 'datetime', 'stock')