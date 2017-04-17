import json

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from worth2.ssnm.models import Supporter
from worth2.ssnm.tests.factories import SupporterFactory
from worth2.main.tests.mixins import LoggedInParticipantTestMixin


class SupporterViewSetTest(LoggedInParticipantTestMixin, APITestCase):
    def test_list(self):
        SupporterFactory(user=self.u)
        SupporterFactory(user=self.u)
        SupporterFactory(user=self.u)
        SupporterFactory()

        r = self.client.get(reverse('supporter-list'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 3)

    def test_retrieve(self):
        supporter = SupporterFactory(user=self.u)
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

    def test_create(self):
        r = self.client.post(
            reverse('supporter-list'),
            data=json.dumps({
                'closeness': 'NC',
                'influence': 'N',
                'name': 'Supporter name',
                'provides_emotional_support': True,
                'provides_practical_support': False,
            }),
            content_type='application/json',
        )
        self.assertEqual(r.status_code, 201)

        pk = r.data.get('id')
        supporter = Supporter.objects.get(pk=pk)
        self.assertEqual(supporter.closeness, 'NC')
        self.assertEqual(supporter.influence, 'N')
        self.assertEqual(supporter.name, 'Supporter name')
        self.assertEqual(supporter.provides_emotional_support, True)
        self.assertEqual(supporter.provides_practical_support, False)


class SupporterViewSetUnAuthedTest(APITestCase):
    def test_list(self):
        SupporterFactory()
        SupporterFactory()

        r = self.client.get(reverse('supporter-list'))
        self.assertEqual(r.status_code, 403)

    def test_retrieve(self):
        supporter = SupporterFactory()
        r = self.client.get(
            reverse('supporter-detail', args=(supporter.pk,))
        )
        self.assertEqual(r.status_code, 403)

    def test_create(self):
        r = self.client.post(
            reverse('supporter-list'),
            {
                'closeness': 'NC',
                'influence': 'N',
                'name': 'Supporter name',
                'provides_emotional_support': True,
                'provides_practical_support': False,
            }
        )

        self.assertEqual(r.status_code, 403)
        self.assertEqual(Supporter.objects.count(), 0)
