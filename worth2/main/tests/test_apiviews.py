from rest_framework.test import APITestCase

from worth2.main.models import Participant
from worth2.main.tests.mixins import LoggedInFacilitatorAPITestMixin


class ParticipantViewSetCreateAuthedTest(
        LoggedInFacilitatorAPITestMixin, APITestCase):
    def test_create(self):
        response = self.client.post(
            '/api/participants/', {'study_id': '777'}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['study_id'], '777')

        participant = Participant.objects.get(study_id='777')
        self.assertEqual(participant.study_id, '777')


class ParticipantViewSetCreateUnAuthedTest(APITestCase):
    def test_create(self):
        response = self.client.post(
            '/api/participants/', {'study_id': '777'}
        )
        self.assertEqual(response.status_code, 403)

        with self.assertRaises(Participant.DoesNotExist):
            Participant.objects.get(study_id='777')
