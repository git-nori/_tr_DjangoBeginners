from django.test import TestCase
from django.urls import reverse, resolve

from boards.views import BoardTopicsListView
from boards.models import Board


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
        self.assertEquals(view.func.view_class, BoardTopicsListView)

    # レスポンス内にHomeへのリンクを含むか判定
    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
