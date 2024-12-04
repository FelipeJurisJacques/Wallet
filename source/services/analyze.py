import datetime
from django.db import connection
from ..models.stock import StockModel
from ..entities.stock import StockEntity
from ..models.forecast import ForecastModel
from ..entities.historic import HistoricEntity
from ..entities.forecast import ForecastEntity
from ..enumerators.quantitative import QuantitativeEnum
from ..models.period import PeriodModel
from ..enumerators.week import WeekEnum
from ..entities.period import PeriodEntity
from ..enumerators.period import PeriodEnum
from ..libraries.query import QueryLib

class AnalyzeService:

    def get_next_week(self, start: datetime.datetime, day: WeekEnum) -> datetime.datetime:
        while start.weekday() != day.value:
            start += datetime.timedelta(days=1)
        return start

    def get_last_period(self, stock: StockEntity, period: PeriodEnum) -> PeriodEntity:
        query = QueryLib()
        query.select()
        query.table('periods')
        query.inner('periods_historical', 'periods_historical.periodmodel_id = periods.id')
        query.inner('historical', 'historical.id = periods_historical.historicmodel_id')
        query.where(f"periods.period = {query.quote(period)}")
        query.where(f"historical.stock_id = {query.quote(stock.id)}")
        result = PeriodModel.objects.raw(query.assemble())
        if result.exists():
            return PeriodEntity(result[0])
        else:
            return None

    def get_all_from_stock(self, stock:StockEntity, origin: QuantitativeEnum) -> list[ForecastEntity]:
        models = ForecastModel.objects.filter(
            nested_historic__stock_id=stock.id,
            origin=origin.value,
        ).select_related(
            'nested_historic'
        ).order_by(
            'nested_historic__date'
        )
        list = []
        for model in models:
            list.append(ForecastEntity(model))
        return list

    def get_from_consecutive_historic(self, historic:HistoricEntity) -> ForecastEntity:
        result = ForecastModel.objects.filter(nested_historic=historic.id)[:1]
        if result.exists():
            return ForecastEntity(result[0])
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