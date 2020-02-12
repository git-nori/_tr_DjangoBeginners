from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, board_topics
from .models import Board


class HomeTests(TestCase):
    # ステータスコードが200を返すか判定する
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # 正しいviewを返すか判定する
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    # ステータスコードが200を返すか判定する
    def test_board_topics_view_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # ステータスコードが404を返すか判定する
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # 正しいviewを返すか判定する
    def test_home_url_resolves_home_view(self):
        view = resolve('/boards/1')
        self.assertEquals(view.func, board_topics)
