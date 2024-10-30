import datetime
from django.db import connection
from ..models.stock import StockModel
from ..models.prophesy_day import ProphesyDayModel
from ..entities.prophesy_day import ProphesyDayEntity

class ProphesyService:

    def get_all_from_stock(self, stock:StockModel) -> list[ProphesyDayEntity]:
        entities = ProphesyDayModel.objects.filter(stock_id=stock.id).order_by('date')
        list = []
        for entity in entities:
            list.append(ProphesyDayEntity(entity))
        return list

    def get_period_from_stock(self, stock:StockModel, limit:int, offset:int) -> list[ProphesyDayEntity]:
        entities = ProphesyDayModel.objects.filter(stock_id=stock.id)[offset:limit]
        list = []
        for entity in entities:
            list.append(ProphesyDayEntity(entity))
        return list

    def get_max_date_from_stock(self, stock:StockModel) -> datetime.datetime:
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