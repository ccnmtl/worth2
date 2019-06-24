from django.contrib.auth.models import User

from worth2.main.tests.factories import UserFactory


class LoggedInSuperuserTestMixin(object):
    def setUp(self):
        self.u = User.objects.create_superuser(
            'superuser', 'admin@example.com', 'test')
        login = self.client.login(username='superuser', password='test')
        assert(login is True)


class LoggedInUserTestMixin(object):
    def setUp(self):
        self.u = UserFactory()
        login = self.client.login(username=self.u.username, password='test')
        assert(login is True)
