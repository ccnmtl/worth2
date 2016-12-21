from smoketest import SmokeTest
from django.contrib.auth.models import User
from .models import Avatar


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = User.objects.all().count()
        # all we care about is not getting an exception
        self.assertTrue(cnt > -1)


class AvatarTest(SmokeTest):
    def test_single_default(self):
        cnt = Avatar.objects.filter(is_default=True).count()
        self.assertTrue(cnt < 2)
