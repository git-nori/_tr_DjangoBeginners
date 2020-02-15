from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, board_topics, new_topic
from .models import Board, Topic, Post
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
    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description={'Django board'})
        User.objects.create_user(username='john', email='john@doe.com', password='123')

    # ステータスコードが200を返すか判定する
    def test_new_topic_view_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # ステータスコードが404を返すか判定する
    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # 正しいviewを返すか判定する
    def test_new_topic_url_resolves_home_view(self):
        view = resolve('/boards/1/new')
        self.assertEquals(view.func, new_topic)

    # レスポンス内にboard_topicsへのリンクを含むか判定
    def test_new_topic_view_contains_navigation_links(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    # リクエストにcsrfトークンを含むか判定
    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    # POSTリクエストが成功した場合、データが作成されているか判定
    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Test message'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    # 空のデータを送った場合、ステータスコードが200を返すか判定する
    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    # バリデーションエラーが発生するデータ送った場合、ステータスコードが200を返すか判定する
    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
