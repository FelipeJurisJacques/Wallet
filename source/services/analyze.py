from ..models.period import PeriodModel
from ..entities.stock import StockEntity
from ..entities.period import PeriodEntity
from ..models.historic import HistoricModel
from ..models.prophesy import ProphesyModel
from ..entities.historic import HistoricEntity
from ..entities.prophesy import ProphesyEntity
from ..libraries.database.fetch import FetchLib
from ..libraries.database.query import QueryLib
from ..enumerators.historic import HistoricEnum

class AnalyzeService:

    def get_all_periods_to_analyze(self, stock: StockEntity = None) -> list[PeriodEntity]:
        query = QueryLib()
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
        list = []
        models = PeriodModel.objects.raw(query.assemble())
        for model in models:
            list.append(PeriodEntity(model))
        return list
    
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

    def get_historical(self, prophesies: list[ProphesyEntity]) -> HistoricEntity:
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