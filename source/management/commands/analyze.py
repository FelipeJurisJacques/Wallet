from source.entities.stock import StockEntity
from source.enumerators.period import PeriodEnum
from source.libraries.forecast import ForecastLib
from source.services.analyze import AnalyzeService
from source.entities.forecast import ForecastEntity
from source.entities.prophesy import ProphesyEntity
from django.core.management.base import BaseCommand
from source.enumerators.historic import HistoricEnum

class Command(BaseCommand):
    help = 'Análisar resultados de previsões quantitativas das ações'
    
    def handle(self, *args, **options):
        total = 0
        stocks = StockEntity.all()
        service = AnalyzeService()
        for stock in stocks:
            self.stdout.write('Análisando professias de ' + stock.name)
            periods = service.get_all_periods_to_analyze(stock)
            for period in periods:
                prophesies = service.get_prophesies(period, HistoricEnum.CLOSE)
                historical = service.get_historical(prophesies)
                if len(prophesies) == 0:
                    continue
                library = ForecastLib()
                library.set_prophesies(prophesies)
                library.set_historical(historical)
                library.handle()
                total += library.persist()
                # break
            break
        print(total)