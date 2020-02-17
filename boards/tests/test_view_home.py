from django.test import TestCase
from django.urls import reverse, resolve

from boards.forms import NewTopicForm
from boards.views import home, board_topics, new_topic
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User


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
