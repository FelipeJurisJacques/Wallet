from datetime import timedelta
from source.enumerators.week import WeekEnum
from source.services.stock import StockService
from source.libraries.prophet import ProphetLib
from source.enumerators.period import PeriodEnum
from source.services.prophesy import ProphesyService
from django.core.management.base import BaseCommand
from source.enumerators.historic import HistoricEnum

class Command(BaseCommand):
    help = 'Realizar professia do histórico das ações'
    
    def handle(self, *args, **options):
        period = PeriodEnum.MONTH
        stock_service = StockService()
        prophesy_service = ProphesyService()
        stocks = stock_service.all()

        for stock in stocks:
            end = prophesy_service.get_max_date_period(stock, period, PeriodEnum.DAY)
            if end is None:
                start = prophesy_service.get_min_date_historic(stock, PeriodEnum.DAY)
                if start is None:
                    continue
                end = prophesy_service.get_next_date(start + timedelta(days=180), WeekEnum.TUESDAY)
            else:
                end = prophesy_service.get_next_date(end, WeekEnum.TUESDAY, period)
            if end is None:
                continue
            start = end - timedelta(days=180)
            while True:
                historical = prophesy_service.get_historical(stock, PeriodEnum.DAY, start, end)
                length = len(historical)
                if length == 0:
                    break
                self.stdout.write(
                    'Processando ' + str(length) + ' ações da empresa ' + stock.name + ' de ' + start.strftime("%d/%m/%Y %H:%M:%S") + ' até ' + end.strftime("%d/%m/%Y %H:%M:%S")
                )
                try:
                    library = ProphetLib([
                        HistoricEnum.CLOSE,
                    ])
                    library.set_historical(historical)
                    library.handle(period)
                    library.persist()
                    library.flush()
                except Exception as error:
                    self.stdout.write('Erro ao processar ações: ' + str(error))
                end = prophesy_service.get_next_date(end, WeekEnum.TUESDAY, period)
                start = end - timedelta(days=180)