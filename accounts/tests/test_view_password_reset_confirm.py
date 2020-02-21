from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase


class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        email = 'test@test.com'
        username = 'test_user'
        password = 'test123'
        user = User.objects.create_user(username=username, email=email, password=password)

        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)
        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.post(url, follow=True)

    # ステータスコードが200を返すか判定する
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # 正しいビューかを判定する
    def test_view_function(self):
        view = resolve('/reset/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)

    # レスポンスにcsrfトークンが含まれているか判定する
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    # レスポンスにフォームが含まれているか判定する
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    # フォームのinput項目が正しく画面に表示されているか確認する
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        email = 'test@test.com'
        username = 'test_user'
        password = 'test123'
        user = User.objects.create_user(username=username, email=email, password=password)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # tokenと異なるパスワードを設定
        user.set_password('changed password')
        user.save()

        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))
