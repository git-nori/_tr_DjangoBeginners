from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, board_topics
from .models import Board


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    # ステータスコードが200を返すか判定する
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # 正しいviewを返すか判定する
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    # レスポンス内にTopicsへのリンクを含むか判定
    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


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

    # レスポンス内にHomeへのリンクを含むか判定
    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
