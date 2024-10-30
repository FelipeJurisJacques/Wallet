from django.db import transaction
from source.services.stock import StockService
from source.libraries.prophet import ProphetLib
from django.core.management.base import BaseCommand
from source.services.prophesy import ProphesyService
from source.services.historical import HistoricalService

class Command(BaseCommand):
    help = 'Realizar professia das informações das ações'
    
    def handle(self, *args, **options):
        stock_service = StockService()
        prophesy_service = ProphesyService()
        historical_service = HistoricalService()

        stocks = stock_service.all()
        library = ProphetLib()
        for stock in stocks:
            historical = historical_service.get_all_from_stock(stock)
            length = len(historical)
            if length == 0:
                continue
            self.stdout.write('Processando ' + str(length) + ' ações da empresa' + stock.name)
            last = prophesy_service.get_max_date_from_stock(stock)
            list = []
            for historic in historical:
                list.append(historic)
                # if last is None:
                #     if 180 > len(list):
                #         continue
                # else:
                if not last is None and last.timestamp() > historic.date.timestamp():
                    continue
                library.set_historical(list)
                library.handle(1)
                try:
                    transaction.set_autocommit(False)
                    library.persist()
                    transaction.commit()
                    transaction.set_autocommit(True)
                    del historic
                    library.flush()
                except Exception as error:
                    transaction.rollback()
                    self.stdout.write('Erro ao salvar profetização das ações: ' + str(error))
                    transaction.set_autocommit(True)
                    del historic
                    library.flush()
                    break
            del last
            del list
            del stock
            del length
            del historical
            break # remover quando os testes forem maiores
        del stocks