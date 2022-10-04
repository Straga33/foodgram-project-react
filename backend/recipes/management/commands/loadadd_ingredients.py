import csv

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Loads ingredients from /data'

    def handle(self, *args, **options):
        with open(
            f'{settings.BASE_DIR}/data/ingredients.csv',
            'r',
            encoding='utf-8',
        ) as file:
            reader = csv.reader(file)
            for value in reader:
                name, measurement_unit = value
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )
        self.stdout.write(
            self.style.SUCCESS('Ингредиенты добавлены')
        )
