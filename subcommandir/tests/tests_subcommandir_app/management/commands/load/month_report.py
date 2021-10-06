from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--type', dest='type', type=int, choices=[0, 1, 2, 3], help='Type of report')

    def handle(self, *args, **options):
        ...
