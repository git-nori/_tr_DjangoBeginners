from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse, resolve
from django.test import TestCase


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    # ステータスコードが200を返すか判定する
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # 正しいビューかを判定する
    def test_view_function(self):
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    # レスポンスにcsrfトークンが含まれているか判定する
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    # レスポンスにフォームが含まれているか判定する
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    # フォームのinput項目が正しく画面に表示されているか確認する
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'test@test.com'
        username = 'test_user'
        password = 'test123'
        User.objects.create_user(username=username, email=email, password=password)
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    # リダイレクト先が正しいか確認する
    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    # パスワードリセットメールが1件送信されるか確認する
    def test_send_password_reset_email(self):
        self.assertEquals(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'dontexist@test.com'})

    # リダイレクト先が正しいか確認する
    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    # パスワードリセットメールが送信されないか確認する
    def test_send_password_reset_email(self):
        self.assertEquals(0, len(mail.outbox))
