from __future__ import unicode_literals

from django.urls import reverse
from django.utils.encoding import smart_text
from rest_framework import status
from rest_framework.test import APITestCase

from worth2.main.models import Participant, WatchedVideo
from worth2.main.tests.factories import (
    ParticipantFactory, WatchedVideoFactory, UserFactory
)
from worth2.main.tests.mixins import (
    LoggedInFacilitatorTestMixin, LoggedInParticipantTestMixin
)


class LoginCheckTest(LoggedInParticipantTestMixin, APITestCase):
    def test_post_no_user(self):
        response = self.client.post(reverse('api-login-check'), {
            'facilitator_username': 'fake user',
            'facilitator_password': 'test',
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'User "fake user" not found')

    def test_post_correct_password(self):
        facilitator = UserFactory(username='facilitator')
        facilitator.set_password('password1')
        facilitator.save()
        response = self.client.post(reverse('api-login-check'), {
            'facilitator_username': 'facilitator',
            'facilitator_password': 'password1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['login_check'], True)

    def test_post_wrong_password(self):
        facilitator = UserFactory(username='facilitator')
        facilitator.set_password('password1')
        facilitator.save()
        response = self.client.post(reverse('api-login-check'), {
            'facilitator_username': 'facilitator',
            'facilitator_password': 'wrong_password',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['login_check'], False)


class ParticipantViewSetTest(
        LoggedInFacilitatorTestMixin, APITestCase):
    def test_create(self):
        study_id = '0122371304632'
        response = self.client.post(
            '/api/participants/', {'study_id': study_id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['study_id'], study_id)

        participant = Participant.objects.get(study_id=study_id)
        self.assertEqual(participant.study_id, study_id)
        self.assertEqual(participant.created_by, self.u)

    def test_update_study_id(self):
        p = ParticipantFactory(study_id='0122371304632')
        study_id = '0122371304631'
        response = self.client.put(
            '/api/participants/' + smart_text(p.pk) + '/',
            {'study_id': study_id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['study_id'], study_id)

        participant = Participant.objects.get(study_id=study_id)
        self.assertEqual(participant.study_id, study_id)

    def test_update_study_id_invalid(self):
        study_id = '0122251304634'
        bad_study_id = '0122371304639'
        p = ParticipantFactory(study_id=study_id)
        response = self.client.put(
            '/api/participants/' + smart_text(p.pk) + '/',
            {'study_id': bad_study_id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('That study ID isn\'t valid.',
                      response.data['study_id'][0])

        with self.assertRaises(Participant.DoesNotExist):
            Participant.objects.get(study_id=bad_study_id)

    def test_update_cohort_id(self):
        study_id = '0122251304631'
        p = ParticipantFactory(study_id=study_id, cohort_id='111')
        response = self.client.put(
            '/api/participants/' + smart_text(p.pk) + '/', {
                'study_id': study_id,
                'cohort_id': '787',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cohort_id'], '787')

        participant = Participant.objects.get(study_id=study_id)
        self.assertEqual(participant.cohort_id, '787')

    def test_update_cohort_id_invalid(self):
        study_id = '0122251304634'
        p = ParticipantFactory(study_id=study_id, cohort_id='111')
        response = self.client.put(
            '/api/participants/' + smart_text(p.pk) + '/', {
                'study_id': study_id,
                'cohort_id': 'j87878',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['cohort_id'],
            ['That cohort ID isn\'t valid. (It needs to be 3 digits)'])

        with self.assertRaises(Participant.DoesNotExist):
            Participant.objects.get(cohort_id='j87878')

    def test_update_archive(self):
        study_id = '0122371304632'
        p = ParticipantFactory(study_id=study_id, is_archived=False)
        response = self.client.put(
            '/api/participants/' + smart_text(p.pk) + '/',
            {'study_id': study_id, 'is_archived': True}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        participant = Participant.objects.get(pk=p.pk)
        self.assertEqual(participant.is_archived, True)


class ParticipantViewSetUnAuthedTest(APITestCase):
    def test_create(self):
        study_id = '0122251304631'
        response = self.client.post(
            '/api/participants/', {'study_id': study_id}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.assertRaises(Participant.DoesNotExist):
            Participant.objects.get(study_id=study_id)

    def test_update_study_id(self):
        study_id = '0122251304631'
        good_study_id = '0122251304632'
        p = ParticipantFactory(study_id=study_id)
        response = self.client.put(
            '/api/participants/' + smart_text(p.pk) + '/',
            {'study_id': good_study_id}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.assertRaises(Participant.DoesNotExist):
            Participant.objects.get(study_id=good_study_id)


class WatchedVideoViewSetUnAuthedTest(APITestCase):
    def test_create(self):
        video_id = 'test_video_id'
        response = self.client.post('/api/watched_videos/',
                                    {'video_id': video_id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.assertRaises(WatchedVideo.DoesNotExist):
            WatchedVideo.objects.get(video_id=video_id)

    def test_list(self):
        r = self.client.get('/api/watched_videos/')
        self.assertEqual(r.status_code, 403)

    def test_retrieve(self):
        response = self.client.get('/api/watched_videos/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class WatchedVideoViewSetTest(
        LoggedInParticipantTestMixin, APITestCase):
    """This endpoint should be accessible to any authenticated user."""

    def test_create(self):
        video_id = 'test_video_id'
        r = self.client.post('/api/watched_videos/', {'video_id': video_id})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        objs = WatchedVideo.objects.filter(user=self.u)
        self.assertEqual(objs.count(), 1)
        self.assertEqual(objs.first().video_id, video_id)

    def test_list(self):
        WatchedVideoFactory(user=self.u, video_id='abc')
        WatchedVideoFactory(user=self.u, video_id='def')
        WatchedVideoFactory(user=self.u, video_id='ghi')

        r = self.client.get('/api/watched_videos/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 3)

    def test_create_duplicate(self):
        video_id = 'test_video_id'
        r = self.client.post('/api/watched_videos/', {'video_id': video_id})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        objs = WatchedVideo.objects.filter(user=self.u)
        self.assertEqual(objs.count(), 1)
        self.assertEqual(objs.first().video_id, video_id)

        # re-run it
        r = self.client.post('/api/watched_videos/', {'video_id': video_id})
        # TODO: this ought to be a 304 Not Modified, not a 201
        # but at the very least, it shouldn't be a 500
        self.assertNotEqual(r.status_code, 500)
