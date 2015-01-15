from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from worth2.ssnm.tests.factories import SupporterFactory
from worth2.main.tests.mixins import LoggedInParticipantTestMixin


class SupporterViewSetTest(LoggedInParticipantTestMixin, APITestCase):
    def test_list(self):
        SupporterFactory(participant=self.participant)
        SupporterFactory(participant=self.participant)
        SupporterFactory(participant=self.participant)
        SupporterFactory()

        r = self.client.get(reverse('supporter-list'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data.get('count'), 3)

    def test_retrieve(self):
        supporter = SupporterFactory(participant=self.participant)
        r = self.client.get(
            reverse('supporter-detail', args=(supporter.pk,))
        )
        self.assertEqual(r.status_code, 200)

    def test_retrieve_only_related_supporters(self):
        supporter = SupporterFactory()
        r = self.client.get(
            reverse('supporter-detail', args=(supporter.pk,))
        )
        self.assertEqual(r.status_code, 404)
