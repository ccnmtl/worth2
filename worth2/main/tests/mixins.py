from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase


# TODO: make this a facilitator login, not just generic user
class LoggedInFacilitatorTestMixin(TestCase):
    def setUp(self):
        self.u = User.objects.create(username='testuser')
        self.u.set_password('test')
        self.u.save()
        self.client.login(username='testuser', password='test')


class LoggedInFacilitatorAPITestMixin(APITestCase):
    def setUp(self):
        self.u = User.objects.create_superuser(
            'testuser', 'admin@example.com', 'test')
        self.client.login(username='testuser', password='test')
