from django.db import models
from .timeline import Timeline

class Analyze(models.Model):
    id = models.AutoField(primary_key=True)
    period = models.IntegerField(db_index=True)
    created = models.IntegerField()
    updated = models.IntegerField()
    timelines = models.ManyToManyField(Timeline, db_index=True)

    class Meta:
        db_table = 'analyzes'