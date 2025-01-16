from .analyze import Analyze
from django.db import models
from .timeline import Timeline

class Prophesy(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField(db_index=True)
    analyze = models.ForeignKey(Analyze, on_delete=models.CASCADE, db_index=True)
    timeline = models.OneToOneField(
        Timeline,
        db_index=True,
        on_delete=models.CASCADE
    )
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
        unique_together = ('type', 'analyze', 'timeline')

