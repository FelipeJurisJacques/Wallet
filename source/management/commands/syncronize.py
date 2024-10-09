import datetime
import yfinance
from django.conf import settings
from source.enumerators.api import ApiEnum
from source.models.stock import StockModel
from source.services.stock import StockService
from django.core.management.base import BaseCommand
from source.services.historical import HistoricalService

class Command(BaseCommand):
    help = 'Carregar informações das APÌs'
    
    def handle(self, *args, **options):
        stock_service = StockService()
        historicalService = HistoricalService()
        yfinance.set_tz_cache_location(settings.YFINANCE_CACHE_DIR)

        self.stdout.write('Verificando asções cadastradas')
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


        end = datetime.datetime.now().strftime('%Y-%m-%d')
        stocks = stock_service.all()
        for stock in stocks:
            start = historicalService.get_max_date(stock).strftime('%Y-%m-%d')
            response = yfinance.download(
                stock.symbol,
                start=start,
                end=end
            )
            if not response.empty:
                for item in response.itertuples():
                    historicalService.add(
                        stock,
                        item.Index,
                        item.Open,
                        item.High,
                        item.Low,
                        item.Close,
                        item.Volume
                    )
