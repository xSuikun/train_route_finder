from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from cities.models import City
from routes.forms import RouteForm
from routes.models import Route
from routes.services import get_graph, get_dfs_paths
from trains.models import Train
from routes import views as routes_views


class RoutesTestCase(TestCase):
    def setUp(self) -> None:
        self.city_A = City.objects.create(name='city_A')
        self.city_B = City.objects.create(name='city_B')
        self.city_C = City.objects.create(name='city_C')
        self.city_D = City.objects.create(name='city_D')
        self.city_E = City.objects.create(name='city_E')
        trains_list = [
            Train(name='train_A', from_city=self.city_A, to_city=self.city_B,
                  travel_time=9),
            Train(name='train_B', from_city=self.city_B, to_city=self.city_D,
                  travel_time=8),
            Train(name='train_C', from_city=self.city_A, to_city=self.city_C,
                  travel_time=7),
            Train(name='train_D', from_city=self.city_C, to_city=self.city_B,
                  travel_time=6),
            Train(name='train_E', from_city=self.city_B, to_city=self.city_E,
                  travel_time=3),
            Train(name='train_F', from_city=self.city_B, to_city=self.city_A,
                  travel_time=11),
            Train(name='train_G', from_city=self.city_A, to_city=self.city_C,
                  travel_time=10),
            Train(name='train_H', from_city=self.city_E, to_city=self.city_D,
                  travel_time=5),
            Train(name='train_I', from_city=self.city_D, to_city=self.city_E,
                  travel_time=4)
        ]
        Train.objects.bulk_create(trains_list)
        self.route_A = Route.objects.create(name='city_A-city_B', travel_time='9', from_city=self.city_A,
                                            to_city=self.city_B)
        self.route_A.trains.add(Train.objects.get(name='train_A').id)

    def test_city_name_duplicate(self):
        """Проверка на совпадение по имени с другим городом"""
        city = City(name='city_A')
        with self.assertRaises(ValidationError):
            city.full_clean()

    def test_train_duplicate(self):
        """"Проверка на полное совпадение с другим поездом"""
        train = Train(name='train_A', from_city=self.city_A, to_city=self.city_B, travel_time=9)
        with self.assertRaises(ValidationError):
            train.full_clean()
        try:
            train.full_clean()
        except ValidationError as e:
            self.assertEqual(e.message_dict['__all__'],
                             ['Поезд с таким маршрутом и временем пути уже существует'])

    def test_train_name_duplicate(self):
        """Проверка на совпадение по имени с другим поездом"""
        train = Train(name='train_B', from_city=self.city_A, to_city=self.city_B, travel_time=100)
        with self.assertRaises(ValidationError):
            train.full_clean()

    def test_train_cities_duplicate(self):
        """Проверка на совпадение точки отбытия с точкой прибытия"""
        train = Train(name='train_AA', from_city=self.city_A, to_city=self.city_A, travel_time=123)
        with self.assertRaises(ValidationError):
            train.full_clean()
        try:
            train.full_clean()
        except ValidationError as e:
            self.assertEqual(e.message_dict,
                             {'__all__': ["Поля 'Откуда' и 'Куда' не могут содержать один и тот же город"]})

    def test_routes_home_view(self):
        response = self.client.get(reverse('routes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='routes/home.html')
        self.assertEqual(response.resolver_match.func.__name__, routes_views.SearchRoutes.as_view().__name__)

    def test_routes_detail_view(self):
        response = self.client.get(reverse('routes:detail', kwargs={'pk': self.city_A.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='routes/route_detail.html')
        self.assertEqual(response.resolver_match.func.__name__, routes_views.RouteDetail.as_view().__name__)

    def test_find_all_routes(self):
        trains = Train.objects.all()
        graph = get_graph(trains)
        all_routes = list(get_dfs_paths(graph, self.city_A.id, self.city_E.id))
        self.assertEqual(len(all_routes), 4)

    def test_valid_find_route_form(self):
        data = {'from_city': self.city_A.id, 'to_city': self.city_B.id, 'travel_time': 9, 'cities': [self.city_E.id]}
        form = RouteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_find_route_form(self):
        data = {'from_city': self.city_A.id, 'to_city': self.city_B.id, 'cities': [self.city_E.id]}
        form = RouteForm(data=data)
        self.assertFalse(form.is_valid())







