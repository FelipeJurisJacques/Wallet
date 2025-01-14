from .period import Period
from django.db import models

class Forecast(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField(db_index=True)
    period = models.OneToOneField(Period, on_delete=models.CASCADE, db_index=True)
    min_date = models.IntegerField()
    max_date = models.IntegerField()
    interval = models.IntegerField()
    min_value = models.DecimalField(max_digits=17, decimal_places=2)
    max_value = models.DecimalField(max_digits=17, decimal_places=2)
    difference = models.DecimalField(max_digits=17, decimal_places=2)
    percentage = models.DecimalField(max_digits=17, decimal_places=2)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'forecasts'