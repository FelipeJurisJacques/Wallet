from datetime import datetime
from source.libraries.database.fetch import Fetch
from source.libraries.database.query import Query
from source.entities.stock import Stock as StockEntity
from source.models.analyze import Analyze as AnalyzeModel
from source.entities.analyze import Analyze as AnalyzeEntity
from source.models.historic import Historic as HistoricModel
from source.models.prophesy import Prophesy as ProphesyModel
from source.models.timeline import Timeline as TimelineModel
from source.entities.forecast import Forecast as ForecastEntity
from source.entities.historic import Historic as HistoricEntity
from source.entities.prophesy import Prophesy as ProphesyEntity
from source.entities.timeline import Timeline as TimelineEntity
from source.enumerators.historic import Historic as HistoricEnum

class Analyze:

    def get_all_periods_to_analyze(self, stock: StockEntity = None, start: datetime = None) -> list[AnalyzeEntity]:
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
            query.where(f'prophesied.date > {Query.quote(start)}')
        list = []
        models = AnalyzeModel.objects.raw(query.assemble())
        for model in models:
            list.append(AnalyzeEntity(model))
        return list
    
    def get_prophesies(self, period: AnalyzeEntity, type: HistoricEnum) -> list[ProphesyEntity]:
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