import pytz
import yfinance
from django.conf import settings
from source.enumerators.api import Api as ApiEnum
from django.core.management.base import BaseCommand
from source.entities.stock import Stock as StockEntity
from source.services.stock import Stock as StockService

class Command(BaseCommand):
    help = 'Registrar ações para processar'
    
    def handle(self, *args, **options):
        service = StockService()
        yfinance.set_tz_cache_location(settings.YFINANCE_CACHE_DIR)

        self.stdout.write('Verificando ações cadastradas')
        symbols = service.all_symbols_to_install()
        for symbol in symbols:
            stock = service.get_by_symbol(symbol)
            if stock is None:
                ticker = yfinance.Ticker(symbol)
                info = ticker.info
                stock = StockEntity()
                stock.api = ApiEnum.YAHOO
                stock.name = info.get('shortName')
                stock.symbol = info.get('symbol')
                stock.industry = info.get('longName')
                stock.currency = info.get('currency')
                stock.timezone = pytz.timezone(info.get('timeZoneFullName'))
                stock.fingerprint = info
                stock.save()
                self.stdout.write(stock.name + ' adicionado')