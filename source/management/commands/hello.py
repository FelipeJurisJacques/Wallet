from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Comando que imprime Hello World'

    def handle(self, *args, **kwargs):
        self.stdout.write('Hello World')
