import yfinance
from datetime import datetime 
from django.conf import settings
from source.enumerators.api import Api as ApiEnum
from django.core.management.base import BaseCommand
from source.services.stock import Stock as StockService
from source.enumerators.period import Period as PeriodEnum
from source.libraries.database.transaction import Transaction
from source.entities.historic import Historic as HistoricEntity
from source.services.historic import Historic as HistoricService
from source.services.monetary.timeline import Timeline as TimelineService

class Command(BaseCommand):
    help = 'Carregar informações das APIs'
    
    def handle(self, *args, **options):
        transaction = Transaction()
        stock_service = StockService()
        timeline_service = TimelineService()
        historic_service = HistoricService()
        yfinance.set_tz_cache_location(settings.YFINANCE_CACHE_DIR)

        self.stdout.write('Baixando ações')
        stocks = stock_service.all_from_api(ApiEnum.YAHOO)
        for stock in stocks:
            self.stdout.write('Baixando ações para da empresa ' + stock.name)
            end = datetime.now(stock.timezone).strftime('%Y-%m-%d')
            start = historic_service.get_max_historical_date(stock, PeriodEnum.DAY).strftime('%Y-%m-%d')
            print(start)
            print(end)
            if end == start:
                continue
            response = yfinance.download(
                stock.symbol,
                start=start,
                end=end
            )
            if not response.empty:
                try:
                    transaction.start()
                    for item in response.itertuples():
                        timeline = timeline_service.get_timeline(stock, PeriodEnum.DAY, item.Index)
                        historic = historic_service.get_historic(timeline)
                        if historic is None:
                            historic = HistoricEntity()
                            historic.timeline = timeline
                        historic.low = item.Low
                        historic.high = item.High
                        historic.open = item.Open
                        historic.close = item.Close
                        historic.volume = item.Volume
                        historic.save()
                    transaction.commit()
                    self.stdout.write('Ações salvas')
                except Exception as error:
                    transaction.rollback()
                    # self.stdout.write('Erro ao salvar ações: ' + str(error))
                    raise error
