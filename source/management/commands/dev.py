import numpy
from source.libraries.log import Log
from source.entities.stock import Stock
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from source.enumerators.period import Period as PeriodEnum
from source.libraries.monetary.simulation import Simulation
from source.libraries.ai.neural_network import NeuralNetwork
from source.services.monetary.timeline import Timeline as TimelineService
from source.services.monetary.historic import Historic as HistoricService
from source.libraries.database.fetch import Fetch
from source.libraries.database.query import Query
import pandas
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import Ridge


class Command(BaseCommand):
    help = 'Testes de desenvolvimento'
    
    def handle(self, *args, **options):
        output = Log(self.stdout, self.stderr)

        service = HistoricService()
        fetch = Fetch()

        stocks = Stock.all()
        ridge_model = Ridge(alpha=0.1)
        map = []
        xs = []
        ys = []
        for stock in stocks:
            query = Query()
            query.table('prophesied')
            query.select([
                'prophesied.yhat',
                'prophesied.yhat_lower',
                'prophesied.yhat_upper',
                'timelines.datetime',
            ])
            query.where(f'timelines.stock_id = {stock.id}')
            query.inner('timelines', 'timelines.id = prophesied.timeline_id')
            x = []
            rows = fetch.all(query)
            index = 0
            dt = None
            for row in rows:
                dt = datetime.fromtimestamp(row['datetime'])
                if dt.weekday() == 5 or dt.weekday() == 6:
                    continue
                # x.append([
                #     # float(index),
                #     float(row['yhat']),
                #     float(row['yhat_lower']),
                #     float(row['yhat_upper']),
                # ])
                x.append(float(row['yhat']))
                index += 1
            if dt is None:
                continue
            query = Query()
            query.limit(len(x))
            query.table('historical')
            query.select([
                'historical.close',
                'timelines.datetime',
            ])
            query.where(f'timelines.stock_id = {stock.id}')
            query.where(f'timelines.datetime >= {dt.timestamp()}')
            query.inner('timelines', 'timelines.id = historical.timeline_id')
            # y = []
            max = 0.0
            min = 1000.0
            rows = fetch.all(query)
            # index = 0
            for row in rows:
                dt = datetime.fromtimestamp(row['datetime'])
                if dt.weekday() == 5 or dt.weekday() == 6:
                    continue
                # y.append([
                #     float(row['close'])
                # ])
                # y.append(float(row['close']))
                # if len(y) >= len(x):
                #     break
                value = float(row['close'])
                if value > max:
                    max = value
                if value < min:
                    min = value
                # index += 1
            xs.append(x)
            ys.append(max)
            map.append({
                'stock': stock.name,
                'max': max,
                'min': min,
            })

            # xx = numpy.array(x)
            # yy = numpy.array(y)
            # # print(f'{xx = }, {yy = }')
            # print(f'{xx.shape = }, {yy.shape = }')
            # model = NeuralNetwork(xx, yy, 10, 1)
            # model.fit(500, 0.01)
            # # model = NeuralNetwork(2, 2, 1)
            # # model.train(xx, yy, 1000)
            # print(model.forward(xx))

            # break


        ridge_model.fit(numpy.array(xs), numpy.array(ys))

        predicted_price = ridge_model.predict(numpy.array(xs))
        for i in range(len(xs)):
            if map[i]['max'] < map[i]['min']:
                continue
            fail = False
            if map[i]['max'] > map[i]['min']:
                if predicted_price[i] < map[i]['min']:
                    fail = True
            output.log(f'{map[i]['stock']}: Previsto {predicted_price[i]} Real {map[i]['max']} Min {map[i]['min']} Falha {fail}')
        print(len(xs))
        return


        # x = []
        # y = []
        # for stock in stocks:
        #     historic = service.get_historical(stock, start, end)
        # ai = NeuralNetwork(2, 2, 1)
        # X = numpy.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        # y = numpy.array([[0], [1], [1], [0]])

        # nn = NeuralNetwork(input_size=2, hidden_size=2, output_size=1)
        # nn.train(X, y)
        # print(nn.forward(X))

        # stocks = Stock.all()
        # service = TimelineService()
        # now = datetime.now()
        # day = now - timedelta(days=365 * 5)
        # dates = []
        # for stock in stocks:
        #     while day.timestamp() < now.timestamp():
        #         if day.weekday() == 5 or day.weekday() == 6:
        #             day += timedelta(days=1)
        #             continue
        #         dt = service.get_timeline(stock, PeriodEnum.DAY, day)
        #         if dt is None:
        #             dates.append(day)
        #         day += timedelta(days=1)
        #     # break
        # for date in dates:
        #     output.log(Log.date(date))
        # output.log('Fim')