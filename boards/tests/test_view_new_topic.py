from django.test import TestCase
from django.urls import reverse, resolve

from boards.forms import NewTopicForm
from boards.views import new_topic
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        self.url = reverse('new_topic', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class NewTopicTests(TestCase):
    def setUp(self):
        username = 'john'
        email = 'john@doe.com'
        password = '123'
        Board.objects.create(name='Django', description={'Django board'})
        User.objects.create_user(username=username, email=email, password=password)
        self.client.login(username=username, password=password)

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

    # 空のデータを送った場合、
    # ステータスコードが200を返すか判定する
    # バリデーションエラーを持っているか判定する
    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

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

    # formのインスタンスが正しいか判定する
    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)
