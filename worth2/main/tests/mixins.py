from django.contrib.auth.models import User

from worth2.main.auth import generate_password
from worth2.main.tests.factories import InactiveUserFactory, ParticipantFactory


# TODO: make this a facilitator login, not just generic superuser
class LoggedInFacilitatorTestMixin(object):
    def setUp(self):
        self.u = User.objects.create_superuser(
            'superuser', 'admin@example.com', 'test')
        login = self.client.login(username='superuser', password='test')
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

        self.u.is_active = False
        self.u.save()
