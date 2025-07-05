import time
import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from publics.models import Public  

User = get_user_model()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, required=False)

    def generate(self, *args, **options):
        count = options.get("count") or 7

        users = list(User.objects.all())
        if not users:
            self.stderr.write("Нет пользователей в базе. Сначала создай пользователей.")
            return

        publics = []
        for i in range(count):
            owner = random.choice(users)
            title = f"Public_{i+1}"
            is_private = random.choice([True, False])
            public = Public(
                owner=owner,
                title=title,
                is_private=is_private
            )
            publics.append(public)
            self.stdout.write(f"Создан паблик {title}")

        Public.objects.bulk_create(publics, ignore_conflicts=True)

        all_publics = Public.objects.filter(title__startswith="Public_")
        for public in all_publics:
            members = random.sample(users, k=min(len(users), random.randint(1, 5)))
            public.members.add(*members)

        self.stdout.write("Все паблики сгенерированы и участники добавлены.")

    def handle(self, *args, **options):
        self.stdout.write("Генерация пабликов началась...")
        start = time.perf_counter()
        self.generate(*args, **options)
        end = time.perf_counter()
        self.stdout.write("Паблики успешно сгенерированы.")
        self.stdout.write(f"Выполнено за {end-start:.2f} сек.")
