from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from worth2.main.models import WatchedVideo
from worth2.main.tests.factories import WatchedVideoFactory, UserFactory
from worth2.main.tests.mixins import LoggedInParticipantTestMixin


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
