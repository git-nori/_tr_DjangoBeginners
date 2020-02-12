from django.test import TestCase
from django.urls import reverse, resolve
from .views import home


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
