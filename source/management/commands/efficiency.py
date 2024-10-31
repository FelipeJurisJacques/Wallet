from django.db import transaction
from source.services.stock import StockService
from django.core.management.base import BaseCommand
from source.services.prophesy import ProphesyService
from source.services.forecast import ForecastService
from source.entities.forecast_day import ForecastDayEntity
from source.enumerators.quantitative import QuantitativeEnum

class Command(BaseCommand):
    help = 'Testes de eficiencia das previsões quantitativas das ações'
    
    def handle(self, *args, **options):
        stock_service = StockService()
        forecast_service = ForecastService()

        stocks = stock_service.all()
        for stock in stocks:
            forecasts = forecast_service.get_all_from_stock(stock, QuantitativeEnum.PROPHESY)
            length = len(forecasts)
            if length == 0:
                continue
            self.stdout.write('Processando ' + str(length) + ' preivisões das ações da empresa' + stock.name)
            max = 1.0
            possible = 1.0
            errors = 0
            losses = 0
            winnings = 0
            for forecast in forecasts:
                if forecast.close_corrected_difference is None:
                    break
                if forecast.close_forecast_difference > 0.0:
                    possible += forecast.close_corrected_difference
                    if forecast.close_corrected_difference > 0.0:
                        winnings += 1
                    else:
                        errors += 1
                        losses += 1
                else:
                    if forecast.close_corrected_difference > 0.0:
                        errors += 1
                if forecast.close_corrected_difference > 0.0:
                    max += forecast.close_corrected_difference
            self.stdout.write('Valor arrecadado ' + str(possible))
            self.stdout.write('Valor arrecadavel ' + str(max))
            self.stdout.write('Ganhos ' + str(winnings))
            self.stdout.write('Perdas ' + str(losses))
            self.stdout.write('Erros ' + str(errors))