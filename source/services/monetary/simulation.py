from datetime import datetime
from source.libraries.database.fetch import Fetch
from source.libraries.database.query import Query
from source.entities.stock import Stock as StockEntity
from source.enumerators.period import Period as PeriodEnum
from source.models.historic import Historic as HistoricModel
from source.entities.historic import Historic as HistoricEntity

class Simulation:

    def get_historic_start_date(self) -> datetime:
        fetch = Fetch()
        query = Query()
        query.limit(1)
        query.select('date')
        query.order('date ASC')
        query.table('historical')
        query.where(f"type = {query.quote(PeriodEnum.DAY)}")
        value = fetch.one(query)
        if value is None:
            return None
        else:
            return datetime.fromtimestamp(value)

    def get_historical(self, stock: StockEntity, start: datetime, end: datetime) -> list[HistoricEntity]:
        query = Query()
        query.select()
        query.order('date ASC')
        query.table('historical')
        query.where(f"date <= {query.quote(end)}")
        query.where(f"date >= {query.quote(start)}")
        query.where(f"stock_id = {query.quote(stock.id)}")
        query.where(f"type = {query.quote(PeriodEnum.DAY)}")
        entities = []
        for model in HistoricModel.objects.raw(query.assemble()):
            entities.append(HistoricEntity(model))
        return entities