from django.core.urlresolvers import reverse
from django.test import TestCase
from pagetree.helpers import get_hierarchy


from worth2.main.tests.factories import (
    AvatarFactory, LocationFactory, ParticipantFactory
)
from worth2.main.tests.mixins import (
    LoggedInFacilitatorTestMixin, LoggedInParticipantTestMixin
)
from worth2.main.models import Participant


class AvatarSelectorTest(LoggedInParticipantTestMixin, TestCase):
    def setUp(self):
        super(AvatarSelectorTest, self).setUp()
        self.avatar1 = AvatarFactory()
        self.avatar2 = AvatarFactory()
        self.avatar3 = AvatarFactory()

    def test_get(self):
        r = self.client.get(reverse('avatar-selector'))
        self.assertEqual(r.status_code, 200)

    def test_participant_with_no_avatar(self):
        h = get_hierarchy('main', '/pages/')
        root = h.get_root()
        root.add_child_section_from_dict({
            'label': 'Section 1',
            'slug': 'section-1',
            'pageblocks': [],
            'children': [],
        })
        r = self.client.get('/pages/section-1')

        # Assert that a participant with no avatar is redirected to the
        # avatar selector when attempting to navigate to pagetree
        self.assertEqual(r.status_code, 302)
        self.assertRedirects(r, reverse('avatar-selector'))

    def test_post(self):
        r = self.client.post(reverse('avatar-selector'), {
            'avatar_id': self.avatar1.pk
        })
        # Refresh the participant from the database
        self.participant = Participant.objects.get(pk=self.participant.pk)

        self.assertEqual(r.status_code, 302)
        self.assertEqual(self.participant.avatar, self.avatar1)


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
        self.assertEqual(r.status_code, 403)

    def test_edit_page(self):
        r = self.client.get("/pages/edit/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_instructor_page(self):
        r = self.client.get("/pages/instructor/section-1/")
        self.assertEqual(r.status_code, 302)


class PagetreeViewTestsLoggedIn(LoggedInFacilitatorTestMixin, TestCase):
    def setUp(self):
        super(PagetreeViewTestsLoggedIn, self).setUp()
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
        self.assertEqual(r.status_code, 200)

    def test_instructor_page(self):
        r = self.client.get("/pages/instructor/section-1/")
        self.assertEqual(r.status_code, 200)


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

    def test_post(self):
        location = LocationFactory()
        participant = ParticipantFactory()
        self.client.post(
            reverse('sign-in-participant'),
            {
                'participant_id': participant.pk,
                'participant_location': location.pk,
                'participant_destination': 'last_completed_activity'
            }
        )
        # FIXME: why does the authenticate() call in
        # views.SignInParticipant return None in this test?
        # self.assertEqual(response.status_code, 200)


class SignInParticipantUnAuthedTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('sign-in-participant'))
        self.assertEqual(response.status_code, 302)
