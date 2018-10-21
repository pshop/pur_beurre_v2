from django.test import TestCase
from django.test import Client
from django.contrib import auth

from .models import CustomUser

class IndexTests(TestCase):

    def test_no_user_logged(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_user_can_login(self):
        CustomUser.objects.create_user(email='mail@gmail.com', password='motdepasse', first_name='moi')

        is_authenticated = self.client.login(username='mail@gmail.com', password='motdepasse')
        self.assertTrue(is_authenticated)

    def test_auth_user_recognized_on_index(self):
        CustomUser.objects.create_user(email='mail@gmail.com', password='motdepasse', first_name='moi')

        self.client.login(username='mail@gmail.com', password='motdepasse')
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)


