from django.db import models
from .period import PeriodModel

class ForecastModel(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField(db_index=True)
    period = models.OneToOneField(PeriodModel, on_delete=models.CASCADE, db_index=True)
    forecast_min_value = models.DecimalField(max_digits=17, decimal_places=2)
    forecast_max_value = models.DecimalField(max_digits=17, decimal_places=2)
    forecast_min_moment = models.IntegerField()
    forecast_max_moment = models.IntegerField()
    forecast_difference = models.DecimalField(max_digits=17, decimal_places=2)
    forecast_percentage = models.DecimalField(max_digits=17, decimal_places=2)
    corrected_min_value = models.DecimalField(
        max_digits=17,
        decimal_places=2,
        null=True,
        blank=True
    )
    corrected_max_value = models.DecimalField(
        max_digits=17,
        decimal_places=2,
        null=True,
        blank=True
    )
    corrected_min_moment = models.IntegerField(
        null=True,
        blank=True
    )
    corrected_max_moment = models.IntegerField(
        null=True,
        blank=True
    )
    corrected_difference = models.DecimalField(
        max_digits=17,
        decimal_places=2,
        null=True,
        blank=True
    )
    corrected_percentage = models.DecimalField(
        max_digits=17,
        decimal_places=2,
        null=True,
        blank=True
    )
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'forecasts'