from ..models.stock import Stock as StockModel
from source.enumerators.api import Api as ApiEnum
from ..entities.stock import Stock as StockEntity

class Stock:

    def all_symbols_to_install(self) -> list[str]:
        results = []
        file = open('bin\stocks.txt', 'r')
        for line in file:
            symbol = line.strip()
            if not symbol == '' and not symbol[0] == '#':
                results.append(symbol)
        file.close()
        return results

    def all_from_api(self, api: ApiEnum) -> list[StockEntity]:
        result = []
        for model in StockModel.objects.filter(api=api.value):
            result.append(StockEntity(model))
        return result

    def get_by_symbol(self, symbol:str) -> StockEntity:
        models = StockModel.objects.filter(symbol=symbol)[:1]
        for model in models:
            return StockEntity(model)
        return None