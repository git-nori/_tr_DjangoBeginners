from django.contrib.auth import views as auth_views
from django.urls import reverse, resolve
from django.test import TestCase


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    # ステータスコードが200を返すか判定する
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # 正しいビューかを判定する
    def test_view_function(self):
        view = resolve('/reset/complete/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)
