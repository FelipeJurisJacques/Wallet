from django.db import models
from .historic import Historic

class Period(models.Model):
    id = models.AutoField(primary_key=True)
    period = models.IntegerField(db_index=True)
    historical = models.ManyToManyField(Historic, db_index=True)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'periods'