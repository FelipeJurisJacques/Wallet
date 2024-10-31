import datetime
from django.db import connection
from ..entities.stock import StockEntity
from ..models.prophesy_day import ProphesyDayModel
from ..entities.prophesy_day import ProphesyDayEntity

class ProphesyService:

    def get_all_from_stock(self, stock:StockEntity) -> list[ProphesyDayEntity]:
        models = ProphesyDayModel.objects.filter(
            last_historic__stock_id=stock.id
        ).select_related(
            'last_historic'
        ).order_by(
            'last_historic__date'
        )
        list = []
        for model in models:
            list.append(ProphesyDayEntity(model))
        return list

    def get_period_from_stock(self, stock:StockEntity, limit:int, offset:int) -> list[ProphesyDayEntity]:
        models = ProphesyDayModel.objects.filter(
            last_historic__stock_id=stock.id
        ).select_related(
            'last_historic'
        )[offset:limit]
        list = []
        for model in models:
            list.append(ProphesyDayEntity(model))
        return list
    
    def get_all_from_stock_up_date(self, stock:StockEntity, date: datetime.datetime) -> list[ProphesyDayEntity]:
        models = ProphesyDayModel.objects.filter(
            last_historic__stock_id=stock.id,
            last_historic__date__gte=date.timestamp
        ).select_related(
            'last_historic'
        ).order_by(
            'last_historic__date'
        )
        list = []
        for model in models:
            list.append(ProphesyDayEntity(model))
        return list

    def get_max_date_from_stock(self, stock:StockEntity) -> datetime.datetime:
        query = "SELECT MAX(historical_day.date) AS date FROM prophesied_day INNER JOIN historical_day ON historical_day.id = prophesied_day.last_historic_id WHERE historical_day.stock_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, [
                stock.id,
            ])
            results = cursor.fetchall()
            for result in results:
                timestamp = result[0]
                if not timestamp is None:
                    return datetime.datetime.fromtimestamp(timestamp)
        return None