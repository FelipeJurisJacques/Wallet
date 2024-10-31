import datetime
from django.db import connection
from ..models.stock import StockModel
from ..models.forecast_day import ForecastDayModel
from ..entities.historic_day import HistoricDayEntity
from ..entities.forecast_day import ForecastDayEntity

class ForecastService:

    def get_from_consecutive_historic(self, historic:HistoricDayEntity) -> ForecastDayEntity:
        result = ForecastDayModel.objects.filter(nested_historic=historic.id)[:1]
        if result.exists():
            return ForecastDayEntity(result[0])
        else:
            return None

    def get_max_date_from_stock(self, stock:StockModel) -> datetime.datetime:
        query = "SELECT MAX(historical_day.date) AS date FROM forecasts_day INNER JOIN historical_day ON historical_day.id = forecasts_day.nested_historic_id WHERE historical_day.stock_id = %s"
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