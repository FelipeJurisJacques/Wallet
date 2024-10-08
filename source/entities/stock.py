from django.db import models

class StockEntity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255, unique=True)
    industry = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)

    class Meta:
        db_table = 'stocks'