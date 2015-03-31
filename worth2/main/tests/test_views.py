from django.core.urlresolvers import reverse
from django.test import TestCase

from pagetree.helpers import get_hierarchy

from worth2.main.tests.factories import (
    AvatarFactory, LocationFactory, ParticipantFactory
)
from worth2.main.tests.mixins import (
    LoggedInFacilitatorTestMixin, LoggedInParticipantTestMixin,
    LoggedInSuperuserTestMixin
)
from worth2.main.models import Participant


class AvatarSelectorBlockTest(LoggedInParticipantTestMixin, TestCase):
    def setUp(self):
        super(AvatarSelectorBlockTest, self).setUp()

        self.avatar1 = AvatarFactory()
        self.avatar2 = AvatarFactory()
        self.avatar3 = AvatarFactory()

        self.h = get_hierarchy('main', '/pages/')
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict({
            'label': 'Avatar Selector Section',
            'slug': 'avatar-selector-section',
            'pageblocks': [{
                'block_type': 'Avatar Selector Block',
            }],
            'children': [],
        })
        self.url = '/pages/avatar-selector-section/'

    def test_get(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Avatar Selector Section')

        self.assertContains(r, 'class="worth-avatars"')
        self.assertContains(r, self.avatar1.image.url)
        self.assertContains(r, self.avatar2.image.url)
        self.assertContains(r, self.avatar3.image.url)

    def test_post(self):
        pageblock = self.root.get_first_child().pageblock_set.first()
        param_name = 'pageblock-%d-avatar-id' % pageblock.pk
        r = self.client.post(self.url, {
            param_name: self.avatar1.pk,
        })

        self.assertEqual(r.status_code, 302)
        participant = Participant.objects.get(pk=self.participant.pk)
        self.assertEqual(participant.avatar, self.avatar1)

        r = self.client.get(self.url)
        self.assertContains(r, 'Here\'s the avatar you selected')
        self.assertContains(r, participant.avatar.image.url)


class BasicTest(TestCase):
    def test_root(self):
        response = self.client.get("/")
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_smoketest(self):
        response = self.client.get("/smoketest/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PASS")


class PagetreeViewTestsLoggedOut(TestCase):
    def setUp(self):
        self.h = get_hierarchy("main", "/pages/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict({
            'label': 'Section 1',
            'slug': 'section-1',
            'pageblocks': [],
            'children': [],
        })

    def test_page(self):
        r = self.client.get('/pages/section-1/')
        self.assertRedirects(r, '/accounts/login/?next=/pages/section-1/')

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
        self.root.add_child_section_from_dict({
            'label': 'Section 1',
            'slug': 'section-1',
            'pageblocks': [],
            'children': [],
        })

    def test_page(self):
        r = self.client.get("/pages/section-1/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Section 1')

    def test_instructor_page(self):
        r = self.client.get("/pages/instructor/section-1/")
        self.assertEqual(r.status_code, 200)


class PagetreeViewTestsAdmin(LoggedInSuperuserTestMixin, TestCase):
    def setUp(self):
        super(PagetreeViewTestsAdmin, self).setUp()
        self.h = get_hierarchy("main", "/pages/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict({
            'label': 'Section 1',
            'slug': 'section-1',
            'pageblocks': [],
            'children': [],
        })

    def test_edit_page(self):
        r = self.client.get("/pages/edit/section-1/")
        self.assertEqual(r.status_code, 200)


class ManageParticipantsAuthedTest(LoggedInFacilitatorTestMixin, TestCase):
    def test_get(self):
        response = self.client.get(reverse('manage-participants'))
        self.assertContains(response, 'Manage Participants')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['active_participants'], [])
        self.assertEqual(response.context['archived_participants'], [])
        self.assertEqual(response.context['cohorts'], [])


class ManageParticipantsUnAuthedTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('manage-participants'))
        self.assertEqual(response.status_code, 302)


class SignInParticipantAuthedTest(LoggedInFacilitatorTestMixin, TestCase):
    def test_get(self):
        response = self.client.get(reverse('sign-in-participant'))
        self.assertContains(response, 'Sign In a Participant')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cohorts'], [])

    def test_get_has_correct_data(self):
        """
        Test that when updating a participant's cohort ID on the
        management page then visiting the sign-in page, the participant
        dropdown has the correct cohort ID.
        """

        p1 = ParticipantFactory(cohort_id='367')
        response = self.client.get(reverse('manage-participants'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, p1.study_id)
        self.assertContains(response, p1.cohort_id)

        p1.cohort_id = '389'
        p1.save()

        response = self.client.get(reverse('sign-in-participant'))
        self.assertContains(response, 'Sign In a Participant')
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response, '<option value="%s"' % p1.cohort_id,
            msg_prefix='Incorrect cohort dropdown cohort ID')
        self.assertEqual(response.context['cohorts'], [p1.cohort_id])

        # TODO: Why is the participant ID dropdown empty here?
        # self.assertContains(response, p1.study_id)
        # self.assertContains(
        #     response, 'data-cohort-id="%s"' % p1.cohort_id,
        #     msg_prefix='Incorrect participant dropdown cohort ID')

    def test_valid_form_submit(self):
        location = LocationFactory()
        participant = ParticipantFactory()
        self.client.post(
            reverse('sign-in-participant'), {
                'participant_id': participant.pk,
                'participant_location': location.pk,
                'participant_destination': 'last_completed_activity',
                'session_type': 'regular',
            }
        )

        # FIXME: why does the authenticate() call in
        # views.SignInParticipant return None in this test?
        # self.assertEqual(response.status_code, 200)
        # form = response.context['form']
        # self.assertTrue(form.is_valid())

    def test_invalid_form_submit(self):
        response = self.client.post(
            reverse('sign-in-participant'), {
                'participant_id': None,
                'participant_location': None,
                'participant_destination': 'last_completed_activity',
                'session_type': 'regular',
            }
        )

        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertContains(response, 'Select a valid choice.')
        self.assertFormError(
            response, 'form', 'participant_id',
            'Select a valid choice. That choice is not one of the ' +
            'available choices.')
        self.assertFormError(
            response, 'form', 'participant_location',
            'Select a valid choice. That choice is not one of the ' +
            'available choices.')

    def test_invalid_form_submit_no_session_type(self):
        location = LocationFactory()
        participant = ParticipantFactory()
        response = self.client.post(
            reverse('sign-in-participant'), {
                'participant_id': participant.pk,
                'participant_location': location.pk,
                'participant_destination': 'last_completed_activity',
            }
        )

        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            response, 'form', 'session_type', 'This field is required.')


class SignInParticipantUnAuthedTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('sign-in-participant'))
        self.assertEqual(response.status_code, 302)


class ParticipantJournalsTest(LoggedInFacilitatorTestMixin, TestCase):
    def setUp(self):
        super(ParticipantJournalsTest, self).setUp()
        self.participant = ParticipantFactory()
        h = get_hierarchy('main', '/pages/')
        root = h.get_root()
        for i in range(1, 6):
            root.add_child_section_from_dict({
                'label': 'Session %d' % i,
                'slug': 'session-%d' % i,
                'pageblocks': [],
                'children': [],
            })

    def test_get_session_1(self):
        session_num = 1
        response = self.client.get(
            reverse('participant-journal',
                    args=(self.participant.pk, session_num)))
        self.assertContains(
            response,
            'Participant %s\'s Journal' % self.participant.study_id)
        self.assertEqual(response.status_code, 200)

    def test_get_session_2(self):
        session_num = 2
        response = self.client.get(
            reverse('participant-journal',
                    args=(self.participant.pk, session_num)))
        self.assertContains(
            response,
            'Participant %s\'s Journal' % self.participant.study_id)
        self.assertEqual(response.status_code, 200)

    def test_get_session_3(self):
        session_num = 3
        response = self.client.get(
            reverse('participant-journal',
                    args=(self.participant.pk, session_num)))
        self.assertContains(
            response,
            'Participant %s\'s Journal' % self.participant.study_id)
        self.assertEqual(response.status_code, 200)

    def test_get_session_4(self):
        session_num = 4
        response = self.client.get(
            reverse('participant-journal',
                    args=(self.participant.pk, session_num)))
        self.assertContains(
            response,
            'Participant %s\'s Journal' % self.participant.study_id)
        self.assertEqual(response.status_code, 200)

    def test_get_session_5(self):
        session_num = 5
        response = self.client.get(
            reverse('participant-journal',
                    args=(self.participant.pk, session_num)))
        self.assertContains(
            response,
            'Participant %s\'s Journal' % self.participant.study_id)
        self.assertEqual(response.status_code, 200)
