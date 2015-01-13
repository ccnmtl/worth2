from django.core.urlresolvers import reverse
from django.test import TestCase

from worth2.main.tests.mixins import LoggedInParticipantTestMixin


class SSNMTest(LoggedInParticipantTestMixin, TestCase):
    def test_get(self):
        r = self.client.get(reverse('ssnm'))
        self.assertEqual(r.status_code, 200)
