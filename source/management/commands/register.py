import pytz
import datetime
import yfinance
from dateutil import tz
from django.conf import settings
from source.enumerators.api import ApiEnum
from source.entities.stock import StockEntity
from source.services.stock import StockService
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Registrar ações para processar'
    
    def handle(self, *args, **options):
        stock_service = StockService()
        yfinance.set_tz_cache_location(settings.YFINANCE_CACHE_DIR)

        self.stdout.write('Verificando ações cadastradas')
        file = open('bin\stocks.txt', 'r')
        for line in file:
            symbol = line.strip()
            stock = stock_service.get_by_symbol(symbol)
            if stock is None:
                ticker = yfinance.Ticker(symbol)
                info = ticker.info
                timezone_edt = pytz.timezone(info.get('timeZoneFullName'))
                current_time = datetime.datetime.now(timezone_edt)
                utc_offset_hours = current_time.utcoffset().total_seconds() / 3600
                stock = StockEntity()
                stock.api = ApiEnum.YAHOO
                stock.name = info.get('shortName')
                stock.symbol = info.get('symbol')
                stock.industry = info.get('longName')
                stock.currency = info.get('currency')
                stock.timezone = utc_offset_hours
                stock.fingerprint = info
                stock.save()
                self.stdout.write(stock.name + ' adicionado')
        file.close()