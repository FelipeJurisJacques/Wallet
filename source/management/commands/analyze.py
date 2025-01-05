from source.libraries.log import LogLib
from source.entities.stock import StockEntity
from source.libraries.forecast import ForecastLib
from source.services.analyze import AnalyzeService
from django.core.management.base import BaseCommand
from source.enumerators.historic import HistoricEnum

class Command(BaseCommand):
    help = 'Análisar resultados de previsões quantitativas das ações'
    
    def handle(self, *args, **options):
        output = LogLib(self.stdout, self.stderr)
        todos = 0
        lucrados = 0
        perdidos = 0
        stocks = StockEntity.all()
        service = AnalyzeService()
        for stock in stocks:
            output.log('Análisando professias de ' + stock.name)
            periods = service.get_all_periods_to_analyze(stock)
            i = 0
            for period in periods:
                prophesies = service.get_prophesies(period, HistoricEnum.CLOSE)
                historical = service.get_historical(prophesies)
                if len(prophesies) == 0:
                    continue
                output.log('De ' + output.date(prophesies[0].date) + ' até ' + output.date(prophesies[-1].date))
                library = ForecastLib()
                library.set_prophesies(prophesies)
                library.set_historical(historical)
                library.handle()
                value1, value2, value3 = library.persist()
                todos += value1
                lucrados += value2
                perdidos += value3
                if perdidos > 3:
                    break
                i += 1
            break
        print(todos, lucrados, perdidos)