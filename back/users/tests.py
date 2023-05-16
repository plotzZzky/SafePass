from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import json


class LoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'temporary',
            'password': '1234x567'}
        self.client = APIClient()
        self.user = User.objects.create_user(**self.credentials)
        self.token = Token.objects.create(user=self.user)  # type:ignore
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.credentials_error = {'username': 'user_error', 'password': '12334555'}

    def test_login_status(self):
        response = self.client.post('/users/login/', self.credentials)
        self.assertEqual(response.status_code, 200)

    def test_login_content_type(self):
        response = self.client.post('/users/login/', self.credentials)
        try:
            j = json.loads(response.content)
        except Exception:
            j = False
        self.assertNotEqual(j, False)

    def test_login_content_result(self):
        response = self.client.post('/users/login/', self.credentials)
        result = json.loads(response.content)
        self.assertEqual(result['token'], self.token.key)

    def test_login_status_error(self):
        response = self.client.post('/users/login/', self.credentials_error)
        self.assertEqual(response.status_code, 300)

    def test_login_status_error_empty(self):
        response = self.client.post('/users/login/', {})
        self.assertEqual(response.status_code, 404)


class RegisterTest(TestCase):
    def setUp(self):
        self.username = 'newuser'
        self.email = 'newuser@mail.com'
        self.password = 12345678

    def post_register(self, username, email, password1, password2):
        response = self.client.post('/users/register/', {
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2,
        })
        return response

    def test_register_status(self):
        response = self.post_register(self.username, self.email, self.password, self.password)
        self.assertEqual(response.status_code, 200)

    def test_register_check_token(self):
        response = self.post_register(self.username, self.email, self.password, self.password)
        user = User.objects.get(username=self.username)
        token = Token.objects.get(user=user)  # type: ignore
        result = json.loads(response.content)
        self.assertEqual(result['token'], token.key)

    def test_register_error_username(self):
        response = self.post_register('aaa', self.email, self.password, self.password)
        self.assertEqual(response.status_code, 300)

    def test_register_error_email(self):
        response = self.post_register(self.username, 'user.mail.com', self.password, self.password)
        self.assertEqual(response.status_code, 300)

    def test_register_error_pwd1(self):
        response = self.post_register(self.username, self.email, '', self.password)
        self.assertEqual(response.status_code, 300)

    def test_register_error_pwd2(self):
        response = self.post_register(self.username, self.email, self.password, '')
        self.assertEqual(response.status_code, 300)

    def test_register_error_pwd_diferent(self):
        response = self.post_register(self.username, self.email, self.password, 1234566)
        self.assertEqual(response.status_code, 300)
