from datetime import datetime
from source.libraries.database.fetch import Fetch
from source.libraries.database.query import Query
from source.models.period import Period as PeriodModel
from source.entities.stock import Stock as StockEntity
from source.entities.period import Period as PeriodEntity
from source.models.historic import Historic as HistoricModel
from source.models.prophesy import Prophesy as ProphesyModel
from source.entities.forecast import Forecast as ForecastEntity
from source.entities.historic import Historic as HistoricEntity
from source.entities.prophesy import Prophesy as ProphesyEntity
from source.enumerators.historic import Historic as HistoricEnum

class Analyze:

    def get_all_periods_to_analyze(self, stock: StockEntity = None, start: datetime = None) -> list[PeriodEntity]:
        query = Query()
        query.table('periods')
        query.group('periods.id')
        query.select('periods.*')
        query.order('periods.created')
        query.where('forecasts.id IS NULL')
        query.left('forecasts', 'forecasts.period_id = periods.id')
        query.inner('prophesied', 'prophesied.period_id = periods.id')
        if stock is not None:
            query.inner('periods_historical', 'periods_historical.periodmodel_id = periods.id')
            query.inner('historical', 'historical.id = periods_historical.historicmodel_id')
            query.where(f'historical.stock_id = {stock.id}')
        if start is not None:
            query.where(f'prophesied.date > {query.quote(start)}')
        list = []
        models = PeriodModel.objects.raw(query.assemble())
        for model in models:
            list.append(PeriodEntity(model))
        return list
    
    def get_prophesies(self, period:PeriodEntity, type: HistoricEnum) -> list[ProphesyEntity]:
        query = Query()
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

    def get_historical(self, forecast: ForecastEntity) -> list[HistoricEntity]:
        fetch = Fetch()
        query = Query()
        query.limit(1)
        query.table('historical')
        query.select([
            'historical.type',
            'historical.stock_id',
        ])
        query.where(f'forecasts.id = {forecast.id}')
        query.inner('forecasts', 'forecasts.period_id = periods.id')
        query.inner('periods', 'periods.id = periods_historical.periodmodel_id')
        query.inner('periods_historical', 'periods_historical.historicmodel_id = historical.id')
        row = fetch.row(query)
        if row is None:
            return []
        end = forecast.max_date.timestamp() + 43200
        start = forecast.min_date.timestamp() - 43200
        query = Query()
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