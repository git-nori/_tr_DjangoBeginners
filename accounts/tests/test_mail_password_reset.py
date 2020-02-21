from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse, resolve
from django.test import TestCase


class PasswordResetMailTests(TestCase):
    def setUp(self):
        self.email_address = 'test@test.com'
        self.username = 'test_user'
        self.password = 'test123'
        User.objects.create_user(username=self.username, email=self.email_address, password=self.password)
        self.response = self.client.post(reverse('password_reset'), {'email': self.email_address})
        self.email = mail.outbox[0]

    # メールの件名が正しいか確認する
    def test_email_subject(self):
        self.assertEquals('[Django Boards] Please reset your password', self.email.subject)

    # メールの本文が正しいか確認する
    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn(self.username, self.email.body)
        self.assertIn(self.email_address, self.email.body)

    # メールの送信先が正しいか確認する
    def test_email_to(self):
        self.assertEquals([self.email_address,], self.email.to)
