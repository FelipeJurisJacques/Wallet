from django.db import models
from .historic_day import HistoricDayModel

class ForecastDayModel(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField(db_index=True)
    nested_historic_id = models.ForeignKey(HistoricDayModel, on_delete=models.CASCADE)
    consecutive_historic_id = models.ForeignKey(HistoricDayModel, on_delete=models.CASCADE, null=True, blank=True)
    open_forecast_difference = models.DecimalField(max_digits=10, decimal_places=2)
    open_forecast_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    close_forecast_difference = models.DecimalField(max_digits=10, decimal_places=2)
    close_forecast_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    open_corrected_difference = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    open_corrected_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    close_corrected_difference = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    close_corrected_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'forecasts_day'