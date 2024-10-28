from django.db import models
from .prophesy import ProphesyModel
from .historic_day import HistoricDayModel

class ProphesyDayModel(models.Model):
    id = models.AutoField(primary_key=True)
    last_historic_id = models.ForeignKey(HistoricDayModel, on_delete=models.CASCADE, db_index=True)
    open_prophesy_id = models.ForeignKey(ProphesyModel, on_delete=models.CASCADE, db_index=True)
    close_prophesy_id = models.ForeignKey(ProphesyModel, on_delete=models.CASCADE, db_index=True)
    created = models.IntegerField()
    updated = models.IntegerField()

    class Meta:
        db_table = 'prophesied_day'

