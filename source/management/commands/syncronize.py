import datetime
import yfinance
from django.conf import settings
from django.db import transaction
from source.enumerators.api import ApiEnum
from source.models.stock import StockModel
from source.services.stock import StockService
from source.models.historic import HistoricModel
from django.core.management.base import BaseCommand
from source.services.historical import HistoricalService

class Command(BaseCommand):
    help = 'Carregar informações das APÌs'
    
    def handle(self, *args, **options):
        stock_service = StockService()
        historicalService = HistoricalService()
        yfinance.set_tz_cache_location(settings.YFINANCE_CACHE_DIR)

        self.stdout.write('Verificando ações cadastradas')
        file = open('bin\stocks.txt', 'r')
        for line in file:
            symbol = line.strip()
            stock = stock_service.get_by_symbol(symbol)
            if stock is None:
                ticker = yfinance.Ticker(symbol)
                info = ticker.info
                stock = StockModel()
                stock.api = ApiEnum.YAHOO
                stock.name = info.get('shortName')
                stock.symbol = info.get('symbol')
                stock.industry = info.get('longName')
                stock.currency = info.get('currency')
                stock.fingerprint = info
                stock.save()
                self.stdout.write(stock.name + ' adicionado')
        file.close()

        self.stdout.write('Baixando ações')
        end = datetime.datetime.now().strftime('%Y-%m-%d')
        stocks = stock_service.all()
        for stock in stocks:
            start = historicalService.get_max_date(stock).strftime('%Y-%m-%d')
            if end == start:
                continue
            response = yfinance.download(
                stock.symbol,
                start=start,
                end=end
            )
            if not response.empty:
                transaction.set_autocommit(False)
                try:
                    for item in response.itertuples():
                        historic = HistoricModel()
                        historic.low = item.Low
                        historic.date = item.Index
                        historic.high = item.High
                        historic.open = item.Open
                        historic.close = item.Close
                        historic.volume = item.Volume
                        historic.stock_id = stock.id
                        historic.save()
                    transaction.commit()
                except Exception:
                    transaction.rollback()
                finally:
                    transaction.set_autocommit(True)
