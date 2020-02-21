from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..views import UserUpdateView
from django.forms import ModelForm


class MyAccountTestCase(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.url = reverse('my_account')


class LoginRequiredMyAccountUpdateView(MyAccountTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UserUpdateViewTests(MyAccountTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/settings/account/')
        self.assertEquals(view.func.view_class, UserUpdateView)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def form_inputs(self):
        self.assertContains(self.response, '<input', 4)


class SuccessfulUserUpdateViewTests(MyAccountTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.first_name = 'changed firstname'
        self.last_name = 'changed lastname'
        self.email = 'changed@test.com'
        self.response = self.client.post(self.url, {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        })

    def test_redirection(self):
        self.assertRedirects(self.response, self.url)

    def test_user_changed(self):
        self.user.refresh_from_db()
        self.assertEquals(self.user.first_name, self.first_name)
        self.assertEquals(self.user.last_name, self.last_name)
        self.assertEquals(self.user.email, self.email)


class InvalidUpdateViewTests(MyAccountTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
