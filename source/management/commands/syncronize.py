import sqlite3
import datetime
import yfinance
from source.services.stock import StockService
from django.core.management.base import BaseCommand
from source.services.historical import HistoricalService

class Command(BaseCommand):
    help = 'Carregar informações das APÌs'
    
    def handle(self, *args, **options):
        stockService = StockService()
        historicalService = HistoricalService()

        end = datetime.datetime.now().strftime('%Y-%m-%d')
        stocks = stockService.all()
        for stock in stocks:
            start = historicalService.getMaxDate(stock).strftime('%Y-%m-%d')
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
