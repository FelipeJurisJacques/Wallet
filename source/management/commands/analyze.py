from django.db import transaction
from source.services.stock import StockService
from django.core.management.base import BaseCommand
from source.services.prophesy import ProphesyService

class Command(BaseCommand):
    help = 'Análisar resultados de previsões quantitativas das ações'
    
    def handle(self, *args, **options):
        stock_service = StockService()
        prophesy_service = ProphesyService()
        

        stocks = stock_service.all()