import datetime
from django.conf import settings
from django.db import transaction
from source.enumerators.api import ApiEnum
from source.models.stock import StockModel
from source.services.stock import StockService
from source.models.historic import HistoricModel
from django.core.management.base import BaseCommand
from source.services.historical import HistoricalService

class Command(BaseCommand):
    help = 'Realizar professia das informações das ações'
    
    def handle(self, *args, **options):
        stock_service = StockService()
        historical_service = HistoricalService()

        stocks = stock_service.all()
        for stock in stocks:
            historical = historical_service.get_all_from_stock(stock)
            total = len(historical)
            if total == 0:
                continue
            self.stdout.write('Processando ' + str(total) + ' ações da empresa' + stock.name)