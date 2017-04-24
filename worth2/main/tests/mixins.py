from django.contrib.auth.models import User

from worth2.main.auth import generate_password
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
        u.set_password(generate_password(u.username))
        u.save()
        self.participant = ParticipantFactory(user=u)
        self.u = self.participant.user

        self.u.is_active = True
        self.u.save()
        login = self.client.login(username=self.u.username,
                                  password=generate_password(self.u.username))
        assert(login is True)
