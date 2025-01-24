from datetime import datetime
from ..models.stock import StockModel
from ..entities.stock import StockEntity
from ..entities.period import PeriodEntity
from ..models.forecast import ForecastModel
from ..models.historic import HistoricModel
from ..models.prophesy import ProphesyModel
from ..entities.forecast import ForecastEntity
from ..entities.historic import HistoricEntity
from ..entities.prophesy import ProphesyEntity
from ..libraries.database.fetch import FetchLib
from ..libraries.database.query import QueryLib
from ..enumerators.historic import HistoricEnum

class StrategyService:

    def get_forecasts(self, start: datetime = None, limit: int = None) -> list[ForecastEntity]:
        query = self._query_forecasts()
        if start is not None:
            query.where(f'min_date > {Query.quote(start)}')
        if limit is not None:
            query.limit(limit)
        result = []
        for model in ForecastModel.objects.raw(query.assemble()):
            result.append(ForecastEntity(model))
        return result

    def get_forecasts_historical(self, start: datetime = None, limit: int = None) -> list[ForecastEntity]:
        query = self._query_forecasts()
        query.where('corrected_difference IS NOT NULL')
        query.where('corrected_percentage IS NOT NULL')
        if start is not None:
            query.where(f'min_date > {Query.quote(start)}')
        if limit is not None:
            query.limit(limit)
        result = []
        for model in ForecastModel.objects.raw(query.assemble()):
            result.append(ForecastEntity(model))
        return result

    def _query_forecasts(self) -> QueryLib:
        query = QueryLib()
        query.select()
        query.table('forecasts')
        query.order([
            'forecast_percentage DESC',
            'interval ASC',
        ])
        query.where('forecast_percentage > 1.0')
        return query

    def get_stock(self, forecast: ForecastEntity):
        query = QueryLib()
        query.limit(1)
        query.table('stocks')
        query.select('stocks.*')
        query.where(f'forecasts.id = {forecast.id}')
        query.inner('historical', 'historical.stock_id = stocks.id')
        query.inner('forecasts', 'forecasts.period_id = periods.id')
        query.inner('periods', 'periods.id = periods_historical.periodmodel_id')
        query.inner('periods_historical', 'periods_historical.historicmodel_id = historical.id')
        for model in StockModel.objects.raw(query.assemble()):
            return StockEntity(model)
        return None
    
    def get_prophesies(self, period:PeriodEntity, type: HistoricEnum) -> list[ProphesyEntity]:
        query = QueryLib()
        query.select()
        query.table('prophesied')
        query.order('prophesied.date')
        query.where(f'prophesied.type = {type.value}')
        query.where(f'prophesied.period_id = {period.id}')
        models = ProphesyModel.objects.raw(query.assemble())
        list = []
        for model in models:
            list.append(ProphesyEntity(model))
        return list

    def get_historical(self, prophesies: list[ProphesyEntity]) -> list[HistoricEntity]:
        if len(prophesies) == 0:
            return []
        fetch = FetchLib()
        query = QueryLib()
        query.limit(1)
        query.table('historical')
        query.select([
            'historical.type',
            'historical.stock_id',
        ])
        query.where(f'periods_historical.periodmodel_id = {prophesies[0].period.id}')
        query.inner('periods_historical', 'periods_historical.historicmodel_id = historical.id')
        row = fetch.row(query)
        if row is None:
            return []
        end = prophesies[-1].date.timestamp() + 43200
        start = prophesies[0].date.timestamp() - 43200
        query = QueryLib()
        query.select()
        query.table('historical')
        query.order('date ASC')
        query.where(f'date <= {end}')
        query.where(f'date >= {start}')
        query.where(f'type = {row.get('type')}')
        query.where(f'stock_id = {row.get('stock_id')}')
        list = []
        for model in HistoricModel.objects.raw(query.assemble()):
            list.append(HistoricEntity(model))
        return list