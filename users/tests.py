from django.test import TestCase

import logging

from .models import CustomUser

log = logging.getLogger(__name__)


class IndexTests(TestCase):

    def setUp(self):
        CustomUser.objects.create_user(email='mail@gmail.com', password='motdepasse', first_name='moi')

    def test_no_user_logged(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_user_can_login(self):
        is_authenticated = self.client.login(username='mail@gmail.com', password='motdepasse')
        self.assertTrue(is_authenticated)

    def test_auth_user_recognized_on_index(self):
        self.client.login(username='mail@gmail.com', password='motdepasse')
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_wrong_password(self):
        is_authenticated = self.client.login(username='mail@gmail.com', password='wrong')
        self.assertFalse(is_authenticated)

    def test_wrong_username(self):
        is_authenticated = self.client.login(username='wrong@gmail.com', password='motdepasse')
        self.assertFalse(is_authenticated)


