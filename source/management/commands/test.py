from source.libraries.log import Log
from django.core.management.base import BaseCommand
from source.libraries.monetary.simulation import Simulation

class Command(BaseCommand):
    help = 'Realiza teste do algoritmo'
    
    def handle(self, *args, **options):
        output = Log(self.stdout, self.stderr)
        self._simulation = Simulation(output, 1000)
        self._simulation.handle()

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