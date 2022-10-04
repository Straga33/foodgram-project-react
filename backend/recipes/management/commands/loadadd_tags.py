
from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Loads tags'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'завтрак', 'color': '#008000', 'slug': 'breakfast'},
            {"name": "обед", 'color': '#FF4500', 'slug': 'lunch'},
            {'name': "ужин", 'color': '#00008B', 'slug': 'dinner'},
            {'name': 'полдник', 'color': '#800080', 'slug': 'snack'}
        ]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(
            self.style.SUCCESS("***Теги добавлены***")
        )
