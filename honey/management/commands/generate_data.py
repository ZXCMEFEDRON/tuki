from django.core.management.base import BaseCommand
from faker import Faker
from honey.models import Group, Honey, Stock, Order, Feedback
import random

class Command(BaseCommand):
    help = 'Генерирует тестовые данные'

    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        group_types = [
            'цветочный','падевый','смешанный','монофлорный','полифлорный','лесной','луговой','горный','степной','таёжный',
        ]
        
        honey_types = [
            'липовый', 'гречишный','акациевый','донниковый','каштановый','клеверный','подсолнечниковый',
            'мятный','эвкалиптовый','рапсовый','майский','июньский','августовский','весенний','осенний',
            'фруктовый','ягодный','кедровый','сосновый','боярышниковый','одуванчиковый','шалфейный',
            'лавандовый','розовый','апельсиновый','гранатовый','миндальный','ванильный','коричный',
            'алтайский','башкирский','кавказский','сибирский','крымский','кубанский','донской','янтарный','ароматный',
        ]
        
        groups = []
        for group_type in group_types:
            group = Group.objects.create(name=group_type + ' мёд')
            groups.append(group)
        self.stdout.write(f'Создано групп: {len(groups)}')
        
        for _ in range(200):
            Honey.objects.create(
                name=random.choice(honey_types) + ' мёд',
                group=random.choice(groups)
            )
        self.stdout.write('Создано товаров: 200')
        
        for _ in range(200):
            Stock.objects.create(
                name=random.choice(honey_types) + ' мёд',
                group=random.choice(groups),
                count=random.randint(0, 500)
            )
        self.stdout.write('Создано остатков: 200')
        
        for _ in range(300):
            Order.objects.create(
                name='Заказ ' + random.choice(honey_types) + ' мёда',
                group=random.choice(groups),
                count=random.randint(1, 100)
            )
        self.stdout.write('Создано заказов: 300')
        
        for _ in range(250):
            Feedback.objects.create(
                name=fake.first_name(),
                group=random.choice(groups),
                comment='Очень вкусный ' + random.choice(honey_types) + ' мёд!'
            )
        self.stdout.write('Создано отзывов: 250')
        
        self.stdout.write(self.style.SUCCESS('Генерация завершена!'))