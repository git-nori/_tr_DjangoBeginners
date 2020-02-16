from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import signup
from django.contrib.auth.models import User
from accounts.forms import SignUpForm


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    # ステータスコードが200を返すか判定する
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # 正しいビューかを判定する
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    # レスポンスにcsrfトークンが含まれているか判定する
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    # レスポンスにフォームが含まれているか判定する
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    # フォームのinput項目が正しく画面に表示されているか確認する
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    # リダイレクト先URLが正しいか判定する
    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    # ユーザーが作成されているか判定する
    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    # ユーザー登録時に登録をしたユーザーが認証済みかを判定する
    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})

    # ステータスコードが正しいか判定する
    def test_signup_status_code(self):
        # バリデーションエラー時にリダイレクトをする
        self.assertEquals(self.response.status_code, 200)

    # バリデーションエラーがあるか判定する
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    # ユーザーが作成されていないことを確認する
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
