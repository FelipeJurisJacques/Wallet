from django.db import transaction
from datetime import datetime, timedelta
from source.enumerators.week import WeekEnum
from source.services.stock import StockService
from source.libraries.prophet import ProphetLib
from source.enumerators.period import PeriodEnum
from source.services.analyze import AnalyzeService
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Análisar resultados de previsões quantitativas das ações'
    
    def handle(self, *args, **options):
        period = PeriodEnum.MONTH
        stock_service = StockService()
        analyze_service = AnalyzeService()
        stocks = stock_service.all()

        for stock in stocks:
            start = analyze_service.get_min_date_historic(stock, PeriodEnum.DAY)
            if start is None:
                continue
            end = analyze_service.get_max_date_period(stock, period, PeriodEnum.DAY)
            if end is None:
                end = analyze_service.get_next_date(start + timedelta(days=180), WeekEnum.TUESDAY, period)
            else:
                end = analyze_service.get_next_date(end, WeekEnum.TUESDAY, period)
            if end is None:
                continue
            while True:
                historical = analyze_service.get_historical(stock, PeriodEnum.DAY, start, end)
                length = len(historical)
                if length == 0:
                    break
                self.stdout.write(
                    'Processando ' + str(length) + ' ações da empresa ' + stock.name + ' de ' + start.strftime("%d/%m/%Y %H:%M:%S") + ' até ' + end.strftime("%d/%m/%Y %H:%M:%S")
                )
                try:
                    library = ProphetLib()
                    library.set_historical(historical)
                    library.handle(period)
                    library.persist()
                    library.flush()
                except Exception as error:
                    self.stdout.write('Erro ao processar ações: ' + str(error))
                end = analyze_service.get_next_date(end, WeekEnum.TUESDAY, period)