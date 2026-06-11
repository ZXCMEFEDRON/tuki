from django.core.management.base import BaseCommand
from faker import Faker
from honey.models import Group, Honey, Stock, Order, Feedback
import random

class Command(BaseCommand):
    help = 'Генерирует тестовые данные'

    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        types = ['липовый', 'гречишный', 'цветочный', 'лесной', 'акациевый', 
            'донниковый', 'клеверный', 'подсолнечниковый', 'мятный', 
            'каштановый', 'горный', 'луговой', 'майский', 'июньский', 'августовский', 'весенний', 'осенний',
            'степной', 'таёжный', 'альпийский', 'полевой', 'садовый',
            'деревенский', 'падевый', 'эспарцетовый', 'фруктовый', 'ягодный', 'эвкалиптовый', 'лавадный', 'кедровый', 'сосновый', 'боярышниковый',
            'чертополоховый', 'одуванчиковый', 'шалфейный', 'лавандовый', 
            'розовый', 'апельсиновый', 'гранатовый', 'миндальный', 'ванильный', 'коричный', 'башкирский', 'алтайский', 'кавказский', 'карпатский', 'сибирский',
            'дальневосточный', 'крымский', 'кубанский', 'донской', 'волжский', 'тёмный', 'светлый', 'янтарный', 'прозрачный', 'кристаллизованный',
            'жидкий', 'густой', 'ароматный']
        
        groups = []
        for _ in range(30):
            group = Group.objects.create(name=random.choice(types) + ' мёд')
            groups.append(group)
        
        for _ in range(200):
            Honey.objects.create(
                name=random.choice(types) + ' мёд',
                group=random.choice(groups)
            )
        
        for _ in range(200):
            Stock.objects.create(
                name=random.choice(types) + ' мёд',
                group=random.choice(groups),
                count=random.randint(0, 500)
            )
        
        for _ in range(300):
            Order.objects.create(
                name='Заказ ' + fake.word(),
                group=random.choice(groups),
                count=random.randint(1, 100)
            )
        
        for _ in range(250):
            Feedback.objects.create(
                name=fake.first_name(),
                group=random.choice(groups),
                comment=fake.sentence(nb_words=5)
            )