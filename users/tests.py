from django.test import TestCase
from django.test import Client
from django.contrib import auth

from core_app.models import CustomUser

def create_valid_user():
    user = CustomUser(email='mail@gmail.com', first_name='pseudo', password='motdepasse')
    user.save()
    return user

def log_user(user):
    pass
# Create your tests here.

class IndexTests(TestCase):

    def test_no_user_logged(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logged_user(self):

        create_valid_user()

        response = self.client.post(
         '/user/login/',
         {'username':'mail@gmail.com',
            'password':'motdepasse'},
         follow=True
        )

        # user = CustomUser.objects.get(email='mail@gmail.com')

        # self.assertEqual(user, None)
        self.assertTrue(response.context['user'].is_authenticated)