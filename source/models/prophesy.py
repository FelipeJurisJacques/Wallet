from django.db import models
from .stock import StockModel

class ProphesyModel(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField()
    stock = models.ForeignKey(StockModel, on_delete=models.CASCADE)
    data_end_date = models.IntegerField()
    data_start_date = models.IntegerField()
    date = models.IntegerField()
    trend = models.DecimalField(max_digits=10, decimal_places=2)
    yhat_lower = models.DecimalField(max_digits=10, decimal_places=2)
    yhat_upper = models.DecimalField(max_digits=10, decimal_places=2)
    trend_lower = models.DecimalField(max_digits=10, decimal_places=2)
    trend_upper = models.DecimalField(max_digits=10, decimal_places=2)
    additive_terms = models.DecimalField(max_digits=10, decimal_places=2)
    additive_terms_lower = models.DecimalField(max_digits=10, decimal_places=2)
    additive_terms_upper = models.DecimalField(max_digits=10, decimal_places=2)
    weekly = models.DecimalField(max_digits=10, decimal_places=2)
    weekly_lower = models.DecimalField(max_digits=10, decimal_places=2)
    weekly_upper = models.DecimalField(max_digits=10, decimal_places=2)
    multiplicative_terms = models.DecimalField(max_digits=10, decimal_places=2)
    multiplicative_terms_lower = models.DecimalField(max_digits=10, decimal_places=2)
    multiplicative_terms_upper = models.DecimalField(max_digits=10, decimal_places=2)
    yhat = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'prophesied'

