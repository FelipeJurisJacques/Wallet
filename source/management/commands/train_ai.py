from source.libraries.log import Log
from source.libraries.monetary.train_ai import TrainAi
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Realiza teste do algoritmo'
    
    def handle(self, *args, **options):
        output = Log(self.stdout, self.stderr)
        self._ai = TrainAi(output)
        self._ai.handle()