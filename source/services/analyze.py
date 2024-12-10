from django.db import connection
from ..models.stock import StockModel
from ..models.period import PeriodModel
from ..enumerators.week import WeekEnum
from datetime import datetime, timedelta
from ..entities.stock import StockEntity
from ..entities.period import PeriodEntity
from ..enumerators.period import PeriodEnum
from ..models.forecast import ForecastModel
from ..models.historic import HistoricModel
from ..entities.forecast import ForecastEntity
from ..entities.historic import HistoricEntity
from ..libraries.database.query import QueryLib
from ..libraries.database.fetch import FetchLib
from ..enumerators.quantitative import QuantitativeEnum

class AnalyzeService:

    def get_next_date(self, start: datetime, day: WeekEnum, period: PeriodEnum) -> datetime:
        if period == PeriodEnum.MONTH:
            start += timedelta(days=30)
        elif period == PeriodEnum.YEAR:
            start += timedelta(days=365)
        else:
            start += timedelta(days=1)
        while start.weekday() != day.value:
            start += timedelta(days=1)
        return start

    def get_last_period(self, stock: StockEntity, period: PeriodEnum) -> PeriodEntity:
        query = QueryLib()
        query.limit(1)
        query.table('periods')
        query.select('periods.*')
        query.order('historical.date DESC')
        query.inner('periods_historical', 'periods_historical.periodmodel_id = periods.id')
        query.inner('historical', 'historical.id = periods_historical.historicmodel_id')
        query.where(f"periods.period = {query.quote(period)}")
        query.where(f"historical.stock_id = {query.quote(stock.id)}")
        result = PeriodModel.objects.raw(query.assemble())
        if result.exists():
            return PeriodEntity(result[0])
        else:
            return None

    def get_max_date_period(self, stock: StockEntity, period: PeriodEnum, historic: PeriodEnum) -> datetime:
        fetch = FetchLib()
        query = QueryLib()
        query.limit(1)
        query.table('periods')
        query.select('historical.date')
        query.order('historical.date DESC')
        query.inner('periods_historical', 'periods_historical.periodmodel_id = periods.id')
        query.inner('historical', 'historical.id = periods_historical.historicmodel_id')
        query.where(f"periods.period = {query.quote(period)}")
        query.where(f"historical.type = {query.quote(historic)}")
        query.where(f"historical.stock_id = {query.quote(stock.id)}")
        timestamp = fetch.one(query.assemble())
        if timestamp is None:
            return None
        else:
            return datetime.fromtimestamp(timestamp)

    def get_max_date_historic(self, stock: StockEntity, historic: PeriodEnum) -> datetime:
        fetch = FetchLib()
        query = QueryLib()
        query.limit(1)
        query.select('date')
        query.order('date DESC')
        query.table('historical')
        query.where(f"type = {query.quote(historic)}")
        query.where(f"stock_id = {query.quote(stock.id)}")
        timestamp = fetch.one(query.assemble())
        if timestamp:
            return datetime.fromtimestamp(timestamp)
        else:
            return None

    def get_min_date_historic(self, stock: StockEntity, historic: PeriodEnum) -> datetime:
        fetch = FetchLib()
        query = QueryLib()
        query.limit(1)
        query.select('date')
        query.order('date ASC')
        query.table('historical')
        query.where(f"type = {query.quote(historic)}")
        query.where(f"stock_id = {query.quote(stock.id)}")
        timestamp = fetch.one(query.assemble())
        if timestamp:
            return datetime.fromtimestamp(timestamp)
        else:
            return None

    def get_historical(self, stock:StockEntity, historic: PeriodEnum, min: datetime, max: datetime):
        list = []
        query = QueryLib()
        query.limit(1)
        query.select('date')
        query.table('historical')
        query.where(f"date >= {query.quote(max.timestamp())}")
        query.where(f"type = {query.quote(historic)}")
        query.where(f"stock_id = {query.quote(stock.id)}")
        fetch = FetchLib()
        timestamp = fetch.one(query.assemble())
        if timestamp:
            query = QueryLib()
            query.select()
            query.order('date ASC')
            query.table('historical')
            query.where(f"date >= {query.quote(min.timestamp())}")
            query.where(f"date <= {query.quote(max.timestamp())}")
            query.where(f"type = {query.quote(historic)}")
            query.where(f"stock_id = {query.quote(stock.id)}")
            for model in HistoricModel.objects.raw(query.assemble()):
                list.append(HistoricEntity(model))
        return list

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

    def get_max_date_from_stock(self, stock:StockModel) -> datetime:
        query = "SELECT MAX(historical_day.date) AS date FROM forecasts_day INNER JOIN historical_day ON historical_day.id = forecasts_day.nested_historic_id WHERE historical_day.stock_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, [
                stock.id,
            ])
            results = cursor.fetchall()
            for result in results:
                timestamp = result[0]
                if not timestamp is None:
                    return datetime.fromtimestamp(timestamp)
        return None