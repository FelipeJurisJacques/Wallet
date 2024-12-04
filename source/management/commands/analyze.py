from django.db import transaction
from source.services.stock import StockService
from source.enumerators.period import PeriodEnum
from source.entities.forecast import ForecastEntity
from django.core.management.base import BaseCommand
from source.services.prophesy import ProphesyService
from source.services.forecast import ForecastService
from source.enumerators.quantitative import QuantitativeEnum

class Command(BaseCommand):
    help = 'Análisar resultados de previsões quantitativas das ações'
    
    def handle(self, *args, **options):
        stock_service = StockService()
        prophesy_service = ProphesyService()
        forecast_service = ForecastService()

        stocks = stock_service.all()
        for stock in stocks:
            prophesied = []
            date = forecast_service.get_max_date_from_stock(stock)
            if date is None:
                prophesied = prophesy_service.get_all_from_stock(stock)
            else:
                prophesied = prophesy_service.get_all_from_stock_up_date(stock, date)
            length = len(prophesied)
            if length == 0:
                continue
            self.stdout.write('Processando ' + str(length) + ' ações da empresa' + stock.name)
            last = None
            try:
                transaction.set_autocommit(False)
                for prophesy in prophesied:
                    historic = prophesy.last_historic
                    if not last is None:
                        last.consecutive_historic = historic
                        previous = forecast.nested_historic
                        last.open_corrected_difference = previous.open - historic.open
                        last.open_corrected_percentage = (previous.open * 100) / historic.open
                        last.close_corrected_difference = previous.close - historic.close
                        last.close_corrected_percentage = (previous.close * 100) / historic.close
                        last.save()
                    forecast = forecast_service.get_from_consecutive_historic(historic)
                    if forecast is None:
                        forecast = ForecastDayEntity()
                        forecast.origin = QuantitativeEnum.PROPHESY
                        forecast.nested_historic = historic
                    open = prophesy.open
                    close = prophesy.close
                    forecast.open_forecast_difference = open.yhat - historic.open
                    forecast.open_forecast_percentage = (open.yhat * 100) / historic.open
                    forecast.close_forecast_difference = close.yhat - historic.close
                    forecast.close_forecast_percentage = (close.yhat * 100) / historic.close
                    last = forecast
                last.save()
                transaction.commit()
                transaction.set_autocommit(True)
            except Exception as error:
                transaction.rollback()
                self.stdout.write('Erro ao salvar previsões das ações: ' + str(error))
                transaction.set_autocommit(True)
                break