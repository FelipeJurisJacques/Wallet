from django.db import models

class StockEntity(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.IntegerField()
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    fingerprint = models.TextField(max_length=65535)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'stocks'