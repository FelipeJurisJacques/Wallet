import datetime
import yfinance
from django.conf import settings
from django.db import transaction
from source.enumerators.api import ApiEnum
from source.services.stock import StockService
from django.core.management.base import BaseCommand
from source.models.historic_day import HistoricDayModel
from source.services.historical import HistoricalService

class Command(BaseCommand):
    help = 'Carregar informações das APIs'
    
    def handle(self, *args, **options):
        stock_service = StockService()
        historical_service = HistoricalService()
        yfinance.set_tz_cache_location(settings.YFINANCE_CACHE_DIR)

        self.stdout.write('Baixando ações')
        stocks = stock_service.all_from_api(ApiEnum.YAHOO)
        for stock in stocks:
            end = datetime.datetime.now(stock.timezone).strftime('%Y-%m-%d')
            start = historical_service.get_max_date_from_stock(stock).strftime('%Y-%m-%d')
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
                transaction.set_autocommit(False)
                try:
                    for item in response.itertuples():
                        historic = historical_service.get_from_stock_date(stock, item.Index)
                        if historic is None:
                            historic = HistoricDayModel()
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
