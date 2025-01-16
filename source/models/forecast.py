from .analyze import Analyze
from django.db import models
from .timeline import Timeline

class Forecast(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField(db_index=True)
    analyze = models.ForeignKey(Analyze, on_delete=models.CASCADE, db_index=True)
    timeline = models.OneToOneField(
        Timeline,
        db_index=True,
        on_delete=models.CASCADE
    )
    min_date = models.IntegerField()
    max_date = models.IntegerField()
    interval = models.IntegerField()
    min_value = models.DecimalField(max_digits=17, decimal_places=2)
    max_value = models.DecimalField(max_digits=17, decimal_places=2)
    difference = models.DecimalField(max_digits=17, decimal_places=2)
    percentage = models.DecimalField(max_digits=17, decimal_places=2)
    quantitative = models.DecimalField(max_digits=17, decimal_places=2)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'forecasts'
        unique_together = ('type', 'analyze', 'timeline')