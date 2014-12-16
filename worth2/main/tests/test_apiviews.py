from rest_framework import status
from rest_framework.test import APITestCase

from worth2.main.models import Participant
from worth2.main.tests.factories import ParticipantFactory
from worth2.main.tests.mixins import LoggedInFacilitatorAPITestMixin


class ParticipantViewSetCreateAuthedTest(
        LoggedInFacilitatorAPITestMixin, APITestCase):
    def test_create(self):
        response = self.client.post(
            '/api/participants/', {'study_id': '777'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['study_id'], '777')

        participant = Participant.objects.get(study_id='777')
        self.assertEqual(participant.study_id, '777')


class ParticipantViewSetCreateUnAuthedTest(APITestCase):
    def test_create(self):
        response = self.client.post(
            '/api/participants/', {'study_id': '777'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.assertRaises(Participant.DoesNotExist):
            Participant.objects.get(study_id='777')


class ParticipantViewSetUpdateAuthedTest(
        LoggedInFacilitatorAPITestMixin, APITestCase):
    def test_update_study_id(self):
        p = ParticipantFactory(study_id='777')
        response = self.client.put(
            '/api/participants/' + unicode(p.pk) + '/',
            {'study_id': '7878'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['study_id'], '7878')

        participant = Participant.objects.get(study_id='7878')
        self.assertEqual(participant.study_id, '7878')

    def test_update_study_id_invalid(self):
        p = ParticipantFactory(study_id='777')
        response = self.client.put(
            '/api/participants/' + unicode(p.pk) + '/',
            {'study_id': 'j87878'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['study_id'],
                         ['That study ID isn\'t valid'])

        with self.assertRaises(Participant.DoesNotExist):
            Participant.objects.get(study_id='j87878')

    def test_update_archive(self):
        p = ParticipantFactory(is_archived=False)
        response = self.client.put(
            '/api/participants/' + unicode(p.pk) + '/',
            {'study_id': p.study_id, 'is_archived': True}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        participant = Participant.objects.get(pk=p.pk)
        self.assertEqual(participant.is_archived, True)


class ParticipantViewSetUpdateUnAuthedTest(APITestCase):
    def test_update_study_id(self):
        p = ParticipantFactory(study_id='777')
        response = self.client.put(
            '/api/participants/' + unicode(p.pk) + '/',
            {'study_id': '7878'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.assertRaises(Participant.DoesNotExist):
            Participant.objects.get(study_id='7878')
