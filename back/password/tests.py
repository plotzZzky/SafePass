from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import Profile
from .pwd import create_db


class PwdTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'temporary',
            'password': '1234x567'}
        self.client = APIClient()
        self.user = User.objects.create_user(**self.credentials)
        self.profile = self.create_profile()
        self.client.login()
        self.token = Token.objects.create(user=self.user)  # type:ignore
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Password
        self.new_title = "password"
        self.url = ""
        self.pwd = self.credentials['password']
        self.pwd_data = {
            "new_title": self.new_title,
            "user": self.user,
            "url": self.url,
            "pwd": self.pwd
        }

    def create_profile(self):
        password = self.credentials['password']
        db = create_db(password)
        profile = Profile.objects.create(user=self.user, db_pwd=password, db=db)  # type:ignore
        return profile

    # get all passwords
    def test_get_all_pwd_status(self):
        response = self.client.get('/pwd/')
        self.assertEqual(response.status_code, 200)

    def test_get_all_pwd_content(self):
        response = self.client.get('/pwd/')
        self.assertEqual(response['content-type'], "application/json")

    # add new plate
    def test_add_pwd_status(self):
        response = self.client.post('/pwd/new/', self.pwd_data)
        self.assertEqual(response.status_code, 200)

    def test_add_plate_content(self):
        self.client.post('/pwd/add/', self.pwd_data)
        try:
            query = Plate.objects.get(number=data['number'])  # type:ignore
        except Plate.DoesNotExist:  # type:ignore
            query = None
        self.assertIsNotNone(query)

    def test_add_pwd_title_error(self):
        data = {
            "new_title": "",
            "user": self.user,
            "url": self.url,
            "pwd": self.pwd
        }
        response = self.client.post('/pwd/new/', data)
        self.assertEqual(response.status_code, 300)

    def test_add_pwd_user(self):
        data = {
            "new_title": self.new_title,
            "user": "",
            "url": self.url,
            "pwd": self.pwd
        }
        response = self.client.post('/pwd/new/', data)
        self.assertEqual(response.status_code, 200)

    def test_add_pwd_url(self):
        data = {
            "new_title": self.new_title,
            "user": self.user,
            "url": "",
            "pwd": self.pwd
        }
        response = self.client.post('/pwd/new/', data)
        self.assertEqual(response.status_code, 200)

    def test_add_pwd_error(self):
        data = {
            "new_title": self.new_title,
            "user": self.user,
            "url": self.url,
            "pwd": ""
        }
        response = self.client.post('/pwd/add/', data)
        self.assertEqual(response.status_code, 404)

    # edit pwd
    def create_and_edit_plate(self, data):
        self.client.post('/pwd/new/', self.pwd_data)
        self.client.post('/pwd/edit/', data)
        response = self.client.get('/pwd/')
        file = response.json()
        return file

    def test_edit_pwd_title(self):
        data = {
            "title": self.new_title,
            "new_title": "new_title",
            "user": self.user,
            "url": self.url,
            "pwd": self.pwd
        }
        file = self.create_and_edit_plate(data)
        result = file['pwd'][0]['title']
        self.assertEqual(result, data['new_title'])

    def test_edit_pwd_user(self):
        data = {
            "title": self.new_title,
            "new_title": self.new_title,
            "user": 'new_user',
            "url": self.url,
            "pwd": self.pwd
        }
        file = self.create_and_edit_plate(data)
        result = file['pwd'][0]['user']
        self.assertEqual(result, data['user'])

    def test_edit_pwd_url(self):
        data = {
            "title": self.new_title,
            "new_title": self.new_title,
            "user": self.user,
            "url": "new_url",
            "pwd": self.pwd
        }
        file = self.create_and_edit_plate(data)
        result = file['pwd'][0]['url']
        self.assertEqual(result, data['url'])

    def test_edit_pwd_password(self):
        data = {
            "title": self.new_title,
            "new_title": self.new_title,
            "user": self.user,
            "url": self.url,
            "pwd": "pwd"
        }
        file = self.create_and_edit_plate(data)
        result = file['pwd'][0]['pwd']
        self.assertEqual(result, data['pwd'])

    def test_edit_pwd_title_error(self):
        data = {
            "title": self.new_title,
            "new_title": "",
            "user": self.user,
            "url": self.url,
            "pwd": self.pwd
        }
        self.client.post('/pwd/new/', self.pwd_data)
        response = self.client.post('/pwd/edit/', data)
        self.assertEqual(response.status_code, 300)

    # Error
    def test_edit_pwd_password_error(self):
        data = {
            "title": self.new_title,
            "new_title": self.new_title,
            "user": self.user,
            "url": self.url,
            "pwd": ""
        }
        self.client.post('/pwd/new/', self.pwd_data)
        response = self.client.post('/pwd/edit/', data)
        self.assertEqual(response.status_code, 300)

    # delete plate
    def test_delete_pwd_status(self):
        data = {
            "title": self.new_title
        }
        self.client.post('/pwd/new/', self.pwd_data)
        response = self.client.delete(f'/pwd/del/', data)
        self.assertEqual(response.status_code, 200)

    def test_delete_pwd_content(self):
        data = {
            "title": self.new_title
        }
        self.client.post('/pwd/new/', self.pwd_data)
        self.client.delete(f'/pwd/del/', data)
        query = self.client.get("/pwd/")
        json = query.json()
        response = json['pwd']
        self.assertEqual(response, {"pwd": []})

    def test_delete_pwd_no_title(self):
        data = {
            "title": ""
        }
        self.client.post('/pwd/new/', self.pwd_data)
        response = self.client.delete(f'/pwd/del/', data)
        self.assertEqual(response.status_code, 404)

    # delete db
    def test_download_db_status(self):
        response = self.client.get("/pwd/get/")
        self.assertEqual(response.status_code, 200)

    def test_download_db_content(self):
        self.client.get("/pwd/get/")
        filename = 'arquivo_recebido.db'
        with open(filename, 'wb') as file:
            self.assertIsNotNone(file)
