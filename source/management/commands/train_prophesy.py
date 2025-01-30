from source.libraries.log import Log
from source.libraries.monetary.train_prophesy import TrainProphesy
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Obtem professias para analise de IA'
    
    def handle(self, *args, **options):
        output = Log(self.stdout, self.stderr)
        self._ai = TrainProphesy(output)
        self._ai.handle()