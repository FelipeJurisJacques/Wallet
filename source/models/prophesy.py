from django.db import models
from .period import PeriodModel

class ProphesyModel(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField(db_index=True)
    period = models.ForeignKey(PeriodModel, on_delete=models.CASCADE, db_index=True)
    increased = models.IntegerField(db_index=True)
    date = models.IntegerField(db_index=True)
    trend = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    yhat_lower = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    yhat_upper = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    trend_lower = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    trend_upper = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    additive_terms = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    additive_terms_lower = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    additive_terms_upper = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    weekly = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    weekly_lower = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    weekly_upper = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    multiplicative_terms = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    multiplicative_terms_lower = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    multiplicative_terms_upper = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    yhat = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'prophesied'
        unique_together = ('type', 'period', 'increased')

