import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from recipe.models import Ingredients

files_dir = os.path.join(settings.BASE_DIR, "..", "data")
file_path = os.path.join(files_dir, 'ingredients.json')


class Command(BaseCommand):
    help = 'loading ingredients from data in json'

    def handle(self, *args, **options):
        try:
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
                for ingredient in data:
                    try:
                        Ingredients.objects.create(
                            name=ingredient["name"],
                            measurement_unit=ingredient[
                                "measurement_unit"
                            ]
                        )
                    except IntegrityError:
                        print(
                            f'Ингридиет {ingredient["name"]} '
                            f'{ingredient["measurement_unit"]} '
                            f'уже есть в базе'
                        )

        except FileNotFoundError:
            raise CommandError('Файл отсутствует в директории data')
