from django.urls import reverse, resolve
from django.test import SimpleTestCase
from .views import RegistrationAPIView, LoginAPIView, LogoutAPIView
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User

class ApiUrlsTests(SimpleTestCase):

    def test_get_register_url_is_resolved(self):
        url = reverse('register_user')
        self.assertEquals(resolve(url).func.view_class, RegistrationAPIView)

    def test_get_login_url_is_resolved(self):
        url = reverse('login_user')
        self.assertEquals(resolve(url).func.view_class, LoginAPIView)

    def test_get_logout_url_is_resolved(self):
        url = reverse('logout_user')
        self.assertEquals(resolve(url).func.view_class, LogoutAPIView)

class LoginAPIViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login_user')
    
    def test_login_endpoint(self):
        u = User.objects.create_user(username='steve', first_name="Steve", last_name="Njuguna", email='steve@gmail.com', password='12345')
        u.is_active = True
        u.save()

        resp = self.client.post(self.url, {'username':'steve', 'password':'12345'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

class RegisterAPIViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register_user')
    
    def test_register_user(self):
        self.user_data = {
            "username": "steve",
            "first_name": "Steve",
            "last_name": "Njuguna",
            "email": "steve@gmail.com",
            "password1": "123456",
            "password2": "123456"
        }

        resp = self.client.post(self.url, self.user_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_if_username_already_exists_dont_signup(self):
        self.user_data = {
            "username": "steve",
            "first_name": "Steve",
            "last_name": "Njuguna",
            "email": "steve@gmail.com",
            "password1": "123456",
            "password2": "123456"
        }
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['username'][0]),
            'A user with that username already exists.',
        )
        username_query = User.objects.filter(username=self.user_saved.username)
        self.assertEqual(username_query.count(), 1)