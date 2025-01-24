from ..models.period import PeriodModel
from ..entities.stock import StockEntity
from ..entities.period import PeriodEntity
from ..libraries.database.query import QueryLib

class PeriodService:

    def get_all_from_stock(self, stock: StockEntity) -> list[PeriodEntity]:
        query = QueryLib()
        query.table('periods')
        query.select('periods.*')
        query.order('historical.date DESC')
        query.inner('periods_historical', 'periods_historical.periodmodel_id = periods.id')
        query.inner('historical', 'historical.id = periods_historical.historicmodel_id')
        query.where(f"historical.stock_id = {Query.quote(stock.id)}")
        list = []
        for model in PeriodModel.objects.raw(query.assemble()):
            list.append(PeriodEntity(model))
        return list