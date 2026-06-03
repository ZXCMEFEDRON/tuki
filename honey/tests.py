from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from honey.models import Group, Honey, Stock, Order, Feedback

# Create your tests here.
class GroupViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        """Тест получения списка групп"""
        groups = baker.make("honey.Group", _quantity=3)

        r = self.client.get('/api/groups/')
        data = r.json()
        
        assert r.status_code == 200
        assert len(data) == 3
        assert data[0]['name'] == groups[0].name
        assert data[0]['id'] == groups[0].id

    def test_create_group(self):
        """Тест создания группы"""
        r = self.client.post("/api/groups/", {
            "name": "Цветочный мед"
        })
        
        assert r.status_code == 201
        new_group_id = r.json()['id']
        
        groups = Group.objects.all()
        assert len(groups) == 1
        
        new_group = Group.objects.filter(id=new_group_id).first()
        assert new_group.name == 'Цветочный мед'

    def test_delete_group(self):
        """Тест удаления группы"""
        groups = baker.make("honey.Group", _quantity=5)
        
        r = self.client.get('/api/groups/')
        assert len(r.json()) == 5
        
        group_id_to_delete = groups[2].id
        r = self.client.delete(f'/api/groups/{group_id_to_delete}/')
        assert r.status_code == 204
        
        r = self.client.get('/api/groups/')
        data = r.json()
        assert len(data) == 4
        assert group_id_to_delete not in [i['id'] for i in data]


class HoneyViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        """Тест получения списка меда"""
        grp = baker.make("honey.Group")
        honeys = baker.make("honey.Honey", group=grp, _quantity=3)

        r = self.client.get('/api/honey/')
        data = r.json()
        
        assert r.status_code == 200
        assert len(data) == 3
        assert data[0]['name'] == honeys[0].name
        assert data[0]['id'] == honeys[0].id
        assert data[0]['group'] == grp.id

    def test_create_honey(self):
        """Тест создания меда"""
        grp = baker.make("honey.Group")

        r = self.client.post("/api/honey/", {
            "name": "Акациевый мед",
            "group": grp.id
        })
        
        assert r.status_code == 201
        new_honey_id = r.json()['id']

        honeys = Honey.objects.all()
        assert len(honeys) == 1

        new_honey = Honey.objects.filter(id=new_honey_id).first()
        assert new_honey.name == 'Акациевый мед'
        assert new_honey.group == grp

    def test_delete_honey(self):
        """Тест удаления меда"""
        grp = baker.make("honey.Group")
        honeys = baker.make("honey.Honey", group=grp, _quantity=10)
        
        r = self.client.get('/api/honey/')
        assert len(r.json()) == 10

        honey_id_to_delete = honeys[3].id
        r = self.client.delete(f'/api/honey/{honey_id_to_delete}/')
        assert r.status_code == 204

        r = self.client.get('/api/honey/')
        data = r.json()
        assert len(data) == 9
        assert honey_id_to_delete not in [i['id'] for i in data]


class StockViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        """Тест получения списка остатков"""
        grp = baker.make("honey.Group")
        stocks = baker.make("honey.Stock", group=grp, _quantity=3)

        r = self.client.get('/api/stock/')
        data = r.json()
        
        assert r.status_code == 200
        assert len(data) == 3
        assert data[0]['name'] == stocks[0].name
        assert data[0]['group'] == grp.id
        assert data[0]['count'] == stocks[0].count

    def test_create_stock(self):
        """Тест создания остатка"""
        grp = baker.make("honey.Group")

        r = self.client.post("/api/stock/", {
            "name": "Липовый мед на складе",
            "group": grp.id,
            "count": 50
        })
        
        assert r.status_code == 201
        new_stock_id = r.json()['id']

        stocks = Stock.objects.all()
        assert len(stocks) == 1

        new_stock = Stock.objects.filter(id=new_stock_id).first()
        assert new_stock.name == 'Липовый мед на складе'
        assert new_stock.count == 50
        assert new_stock.group == grp

    def test_delete_stock(self):
        """Тест удаления остатка"""
        grp = baker.make("honey.Group")
        stocks = baker.make("honey.Stock", group=grp, _quantity=5)
        
        r = self.client.get('/api/stock/')
        assert len(r.json()) == 5

        stock_id_to_delete = stocks[2].id
        r = self.client.delete(f'/api/stock/{stock_id_to_delete}/')
        assert r.status_code == 204

        r = self.client.get('/api/stock/')
        assert len(r.json()) == 4
        assert stock_id_to_delete not in [i['id'] for i in r.json()]


class OrderViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        """Тест получения списка заказов"""
        grp = baker.make("honey.Group")
        orders = baker.make("honey.Order", group=grp, _quantity=3)

        r = self.client.get('/api/orders/')
        data = r.json()
        
        assert r.status_code == 200
        assert len(data) == 3
        assert data[0]['name'] == orders[0].name
        assert data[0]['group'] == grp.id
        assert data[0]['count'] == orders[0].count

    def test_create_order(self):
        """Тест создания заказа"""
        grp = baker.make("honey.Group")

        r = self.client.post("/api/orders/", {
            "name": "Заказ на гречишный мед",
            "group": grp.id,
            "count": 20
        })
        
        assert r.status_code == 201
        new_order_id = r.json()['id']

        orders = Order.objects.all()
        assert len(orders) == 1

        new_order = Order.objects.filter(id=new_order_id).first()
        assert new_order.name == 'Заказ на гречишный мед'
        assert new_order.count == 20
        assert new_order.group == grp

    def test_delete_order(self):
        """Тест удаления заказа"""
        grp = baker.make("honey.Group")
        orders = baker.make("honey.Order", group=grp, _quantity=5)
        
        r = self.client.get('/api/orders/')
        assert len(r.json()) == 5

        order_id_to_delete = orders[3].id
        r = self.client.delete(f'/api/orders/{order_id_to_delete}/')
        assert r.status_code == 204

        r = self.client.get('/api/orders/')
        assert len(r.json()) == 4
        assert order_id_to_delete not in [i['id'] for i in r.json()]


class FeedbackViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        """Тест получения списка отзывов"""
        grp = baker.make("honey.Group")
        feedbacks = baker.make("honey.Feedback", group=grp, _quantity=3)

        r = self.client.get('/api/feedback/')
        data = r.json()
        
        assert r.status_code == 200
        assert len(data) == 3
        assert data[0]['name'] == feedbacks[0].name
        assert data[0]['group'] == grp.id
        assert data[0]['comment'] == feedbacks[0].comment

    def test_create_feedback(self):
        """Тест создания отзыва"""
        grp = baker.make("honey.Group")

        r = self.client.post("/api/feedback/", {
            "name": "Отзыв покупателя",
            "group": grp.id,
            "comment": "Отличный мёд, буду заказывать ещё!"
        })
        
        assert r.status_code == 201
        new_feedback_id = r.json()['id']

        feedbacks = Feedback.objects.all()
        assert len(feedbacks) == 1

        new_feedback = Feedback.objects.filter(id=new_feedback_id).first()
        assert new_feedback.name == 'Отзыв покупателя'
        assert new_feedback.comment == 'Отличный мёд, буду заказывать ещё!'
        assert new_feedback.group == grp

    def test_delete_feedback(self):
        """Тест удаления отзыва"""
        grp = baker.make("honey.Group")
        feedbacks = baker.make("honey.Feedback", group=grp, _quantity=5)
        
        r = self.client.get('/api/feedback/')
        assert len(r.json()) == 5

        feedback_id_to_delete = feedbacks[2].id
        r = self.client.delete(f'/api/feedback/{feedback_id_to_delete}/')
        assert r.status_code == 204

        r = self.client.get('/api/feedback/')
        assert len(r.json()) == 4
        assert feedback_id_to_delete not in [i['id'] for i in r.json()]
        
        #grp = Group.objects.create(
        #    name="Цветочный"
        #)

    #     honey = Honey.objects.create(
    #         name="Акациевый мед",
    #         group=grp,
    #     )

    #     r = self.client.get('/api/honey/')
    #     data = r.json()
    #     print(data)

    #     assert honey.name == data[0]['name']
    #     assert honey.id == data[0]['id']
    #     assert honey.group.id == data[0]['group']
    #     assert len(data) == 1

    # def test_crerate_honey(self):
    #     grp = Group.objects.create(
    #         name="Цветочный"
    #     )

    #     r = self.client.post("/api/honey/", {
    #         "name": "Название",
    #         "group": grp.id
    #     })

    #     new_honey_id = r.json()['id']

    #     honey = Honey.objects.all()
    #     assert len(honey) == 1

    #     new_honey = Honey.objects.filter(id=new_honey_id).first()
    #     assert new_honey.name == 'Название'
    #     assert new_honey.group == grp