from django.db import models
from .timeline import Timeline

class Historic(models.Model):
    id = models.AutoField(primary_key=True)
    open = models.DecimalField(max_digits=17, decimal_places=2)
    high = models.DecimalField(max_digits=17, decimal_places=2)
    low = models.DecimalField(max_digits=17, decimal_places=2)
    close = models.DecimalField(max_digits=17, decimal_places=2)
    volume = models.IntegerField()
    created = models.IntegerField()
    updated = models.IntegerField()
    timeline = models.OneToOneField(
        Timeline,
        unique=True,
        db_index=True,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'historical'