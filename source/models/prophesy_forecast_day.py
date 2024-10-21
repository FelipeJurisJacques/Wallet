from django.db import models
from .stock import StockModel
from .historic_day import HistoricDayModel
from .prophesy_day import ProphesyDayModel

class ProphesyForecastDayModel(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.IntegerField(db_index=True)
    type = models.IntegerField(db_index=True)
    stock_id = models.ForeignKey(StockModel, on_delete=models.CASCADE, db_index=True)
    historic_id = models.ForeignKey(HistoricDayModel, on_delete=models.CASCADE, null=True, blank=True)
    prophesy_id = models.ForeignKey(ProphesyDayModel, on_delete=models.CASCADE)
    value_historic = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    value_forecast = models.DecimalField(max_digits=10, decimal_places=2)
    difference_historic = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage_historic = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    difference_forecast = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_forecast = models.DecimalField(max_digits=10, decimal_places=2)
    qualitative_forecast = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantitative_forecast = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'prophesy_forecasts_day'