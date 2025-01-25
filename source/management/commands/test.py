from source.libraries.log import Log
from django.core.management.base import BaseCommand
from source.libraries.monetary.simulation import Simulation

class Command(BaseCommand):
    help = 'Realiza teste do algoritmo'
    
    def handle(self, *args, **options):
        output = Log(self.stdout, self.stderr)
        self._simulation = Simulation(output, 1000)
        self._simulation.handle()