from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User


class PasswordChangeTests(TestCase):
    def setUp(self, data={}):
        email = 'test@test.com'
        username = 'test_user'
        password = 'old_password'
        self.user = User.objects.create_user(username=username, email=email, password=password)
        self.url = reverse('password_change')
        self.client.login(username=username, password=password)
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTests):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_change(self):
        self.user.refresh_from_db()  # userのデータをリロードする
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTests):
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
