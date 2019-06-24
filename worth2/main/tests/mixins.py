from django.contrib.auth.models import User

from worth2.main.tests.factories import (
    InactiveUserFactory, ParticipantFactory, UserFactory
)


class LoggedInSuperuserTestMixin(object):
    def setUp(self):
        self.u = User.objects.create_superuser(
            'superuser', 'admin@example.com', 'test')
        login = self.client.login(username='superuser', password='test')
        assert(login is True)


class LoggedInFacilitatorTestMixin(object):
    def setUp(self):
        self.u = UserFactory(username='test_facilitator')
        self.u.set_password('test')
        self.u.save()
        login = self.client.login(username='test_facilitator',
                                  password='test')
        assert(login is True)


class LoggedInParticipantTestMixin(object):
    def setUp(self):
        u = InactiveUserFactory()
        u.set_password('test')
        u.save()
        self.participant = ParticipantFactory(user=u)
        self.u = self.participant.user

        self.u.save()
        login = self.client.login(username=self.u.username, password='test')
        assert(login is True)


class LoggedInUserTestMixin(object):
    def setUp(self):
        self.u = UserFactory()
        login = self.client.login(username=self.u.username, password='test')
        assert(login is True)
