from datetime import timedelta
from source.libraries.log import Log
from source.enumerators.api import Api as ApiEnum
from django.core.management.base import BaseCommand
from source.enumerators.week import Week as WeekEnum
from source.entities.stock import Stock as StockEntity
from source.services.stock import Stock as StockService
from source.enumerators.period import Period as PeriodEnum
from source.enumerators.historic import Historic as HistoricEnum
from source.libraries.monetary.analyze import Analyze as AnalyzeLib
from source.libraries.monetary.prophet import Prophet as ProphetLib
from source.libraries.monetary.forecast import Forecast as ForecastLib
from source.services.monetary.timeline import Timeline as TimelineService
# from source.services.analyze import AnalyzeService
# from source.services.prophesy import ProphesyService
# from source.services.strategy import StrategyService

class Command(BaseCommand):
    help = 'Realiza teste do algoritmo'
    
    def handle(self, *args, **options):
        days = 100
        next_date = None
        output = Log(self.stdout, self.stderr)
        forecast = ForecastLib()
        timeline_service = TimelineService()

        # obtem empresas
        stocks = StockEntity.all()
        if len(stocks) == 0:
            output.log('Nenhuma empresa cadastrada')
            return

        # obtem data de inicio
        start = timeline_service.get_min_datetime(PeriodEnum.DAY)
        if start is None:
            output.log('Nenhuma data de inicio')
            return
        end = start + timedelta(days=30)
        output.log('Análisando ações de ' + Log.date(start) + ' até ' + Log.date(end))

        # analisa acoes das empresas
        analyze = AnalyzeLib()
        analyze.set_stocks(stocks, start, end)
        analyze.handle()

        # stock_service = StockService()
        # analyze_service = AnalyzeService()
        # prophesy_service = ProphesyService()
        # strategy_service = StrategyService()

        # output.log('Eliminado dados do banco de dados')
        # prophesy_service.clear_periods()
        # output.log('Teste com o valor inicial de ' + str(money))

        # testing = True
        # while testing:
        #     testing = False

        #     for stock in stocks:
        #         end = next_date
        #         start = None
        #         if end is None:
        #             start = prophesy_service.get_min_date_historic(stock, PeriodEnum.DAY)
        #             if start is None:
        #                 continue
        #             end = prophesy_service.get_next_date(start + timedelta(days=days), WeekEnum.TUESDAY)
        #         if end is None:
        #             continue
        #         if start is None:
        #             start = end - timedelta(days=days)
        #         historical = prophesy_service.get_historical(stock, PeriodEnum.DAY, start, end)
        #         length = len(historical)
        #         if length == 0:
        #             continue
        #         testing = True
        #         output.log(
        #             'Processando ' + str(length) + ' ações da empresa ' + stock.name + ' de ' + output.date(start) + ' até ' + output.date(end)
        #         )
        #         prophesy.set_historical(historical)
        #         prophesy.handle(PeriodEnum.MONTH)
        #         prophesy.persist()
        #         prophesy.flush()

        #     for stock in stocks:
        #         output.log('Análisando professias de ' + stock.name)
        #         periods = analyze_service.get_all_periods_to_analyze(stock, next_date)
        #         for period in periods:
        #             prophesies = analyze_service.get_prophesies(period, HistoricEnum.CLOSE)
        #             historical = analyze_service.get_historical(prophesies)
        #             if len(prophesies) == 0:
        #                 continue
        #             output.log('De ' + output.date(prophesies[0].date) + ' até ' + output.date(prophesies[-1].date))
        #             forecast.set_prophesies(prophesies)
        #             forecast.set_historical(historical)
        #             forecast.handle()
        #             forecast.persist()
        #             forecast.flush()

        #     forecasts = strategy_service.get_forecasts_historical(next_date)
        #     if len(forecasts) == 0:
        #         output.log('Sem opões de investimento')
        #         if next_date is None:
        #             next_date = end
        #         next_date += timedelta(days=15)
        #     else:
        #         entity = None
        #         for e in forecasts:
        #             if entity is None:
        #                 entity = e
        #             if e.min_date < entity.min_date:
        #                 entity = e
        #         next_date = entity.max_date
        #         analyze.set_forecast(entity)
        #         stock = strategy_service.get_stock(entity)
        #         output.log('Investindo em ' + stock.name + ' até ' + output.date(next_date) + ' com valor estimado ' + str(entity.percentage) + '%')
        #         output.log('Valor ' + output.money(analyze.result()))