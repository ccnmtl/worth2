from django.core.urlresolvers import reverse
from django.test import TestCase
from pagetree.helpers import get_hierarchy
from django.contrib.auth.models import User

from worth2.main.models import Participant
from worth2.main.tests.mixins import LoggedInFacilitatorTestMixin
from worth2.main.tests.factories import ParticipantFactory


class BasicTest(TestCase):
    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_smoketest(self):
        response = self.client.get("/smoketest/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PASS")


class PagetreeViewTestsLoggedOut(TestCase):
    def setUp(self):
        self.h = get_hierarchy("main", "/pages/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })

    def test_page(self):
        r = self.client.get("/pages/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_edit_page(self):
        r = self.client.get("/pages/edit/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_instructor_page(self):
        r = self.client.get("/pages/instructor/section-1/")
        self.assertEqual(r.status_code, 302)


class PagetreeViewTestsLoggedIn(TestCase):
    def setUp(self):
        self.h = get_hierarchy("main", "/pages/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.client.login(username="testuser", password="test")

    def test_page(self):
        r = self.client.get("/pages/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_edit_page(self):
        r = self.client.get("/pages/edit/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_instructor_page(self):
        r = self.client.get("/pages/instructor/section-1/")
        self.assertEqual(r.status_code, 200)


class ParticipantCreateAuthedTest(LoggedInFacilitatorTestMixin, TestCase):
    def test_post(self):
        response = self.client.post(
            reverse('participant-create'),
            {'study_id': '777'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        participant = Participant.objects.get(study_id='777')
        self.assertEqual(participant.study_id, '777')


class ParticipantCreateUnAuthedTest(TestCase):
    def test_post(self):
        response = self.client.post(
            reverse('participant-create'),
            {'study_id': '777'}
        )
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(Participant.DoesNotExist):
            Participant.objects.get(study_id='777')


class ParticipantUpdateAuthedTest(LoggedInFacilitatorTestMixin, TestCase):
    def test_valid_study_id(self):
        participant = ParticipantFactory()
        response = self.client.post(
            reverse('participant-update', args=(participant.pk,)),
            {'study_id': '77666'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '77666')

        # Need to get the participant from the db again to see the change
        refreshed_participant = Participant.objects.get(pk=participant.pk)
        self.assertEqual(refreshed_participant.study_id, '77666')

    def test_post_invalid_study_id(self):
        participant = ParticipantFactory()
        response = self.client.post(
            reverse('participant-update',
                    args=(participant.pk,)),
            {'study_id': 'invalid study id'},
            follow=True
        )
        self.assertNotEqual(participant.study_id, 'invalid study id')
        self.assertContains(response, 'That study ID isn&#39;t valid')

    def test_archive(self):
        participant = ParticipantFactory()
        self.assertEqual(participant.is_archived, False)

        self.client.post(
            reverse('participant-update', args=(participant.pk,)),
            {'study_id': participant.study_id,
             'is_archived': 'true'}
        )

        # Need to get the participant from the db again to see the change
        refreshed_participant = Participant.objects.get(pk=participant.pk)
        self.assertEqual(refreshed_participant.is_archived, True)


class ParticipantUpdateUnAuthedTest(TestCase):
    def setUp(self):
        self.participant = ParticipantFactory()

    def test_post(self):
        response = self.client.post(
            reverse('participant-update',
                    args=(self.participant.pk,)),
            dict(study_id='77666')
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(self.participant.study_id, '77666')


class ManageParticipantsAuthedTest(LoggedInFacilitatorTestMixin, TestCase):
    def test_get(self):
        response = self.client.get(reverse('manage-participants'))
        self.assertContains(response, 'Manage Participants')
        self.assertEqual(response.status_code, 200)


class ManageParticipantsUnAuthedTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('manage-participants'))
        self.assertEqual(response.status_code, 302)


class SignInParticipantAuthedTest(LoggedInFacilitatorTestMixin, TestCase):
    def test_get(self):
        response = self.client.get(reverse('sign-in-participant'))
        self.assertContains(response, 'Sign In')
        self.assertEqual(response.status_code, 200)


class SignInParticipantUnAuthedTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('sign-in-participant'))
        self.assertEqual(response.status_code, 302)
