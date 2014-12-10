from django.contrib.auth.models import User


# TODO: make this a facilitator login, not just generic superuser
class LoggedInFacilitatorTestMixin(object):
    def setUp(self):
        self.u = User.objects.create_superuser(
            'superuser', 'admin@example.com', 'test')
        self.client.login(username='superuser', password='test')
