from django.core.urlresolvers import reverse
from django.test import TestCase

from pagetree.helpers import get_hierarchy
from pagetree.models import Hierarchy, Section, UserPageVisit

from worth2.main.auth import generate_password
from worth2.main.tests.factories import (
    AvatarFactory, LocationFactory, ParticipantFactory, WorthModuleFactory
)
from worth2.main.tests.mixins import (
    LoggedInFacilitatorTestMixin, LoggedInParticipantTestMixin,
    LoggedInSuperuserTestMixin
)
from worth2.main.models import Encounter, Participant


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


class SignInParticipantTest(LoggedInFacilitatorTestMixin, TestCase):
    def setUp(self):
        super(SignInParticipantTest, self).setUp()

        WorthModuleFactory('main', '/pages/')
        self.hierarchy = Hierarchy.objects.get(name='main')
        self.module1 = Section.objects.get(slug='session-1')
        self.module2 = Section.objects.get(slug='session-2')
        self.module3 = Section.objects.get(slug='session-3')
        self.module4 = Section.objects.get(slug='session-4')

        self.p1 = ParticipantFactory()
        self.p2 = ParticipantFactory()
        self.p3 = ParticipantFactory()

        self.location = LocationFactory()

    def test_get(self):
        response = self.client.get(reverse('sign-in-participant'))
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
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response, '<option value="%s"' % '389',
            msg_prefix='Incorrect cohort dropdown cohort ID')
        self.assertEqual(response.context['cohorts'], [p1.cohort_id])

        self.assertEqual(
            response.context['form']['participant_id'].field.queryset.filter(
                study_id=p1.study_id).count(), 1)
        self.assertContains(response, p1.study_id)
        self.assertContains(
            response, 'data-cohort-id="%s"' % p1.cohort_id,
            msg_prefix='Incorrect participant dropdown cohort ID')

    def test_valid_form_submit_next_new_session_for_new_participant(self):
        """
        Test that a facilitator can log in a newly created participant that
        hasn't accessed any pages yet.
        """
        participant = ParticipantFactory()

        password = generate_password(participant.user.username)
        participant.user.set_password(password)
        participant.user.save()
        response = self.client.post(
            reverse('sign-in-participant'), {
                'participant_id': participant.pk,
                'participant_location': self.location.pk,
                'participant_destination': 'next_new_session',
                'session_type': 'regular',
            }
        )

        self.assertEqual(response.status_code, 302)

        encounter = Encounter.objects.first()
        self.assertEqual(encounter.facilitator, self.u)
        self.assertEqual(encounter.participant, participant)
        self.assertEqual(encounter.location, self.location)
        self.assertEqual(encounter.session_type, 'regular')
        self.assertEqual(encounter.section, self.module1)
        self.assertEqual(encounter.section, participant.next_module_section())

        self.assertTrue(response.url.endswith('/pages/session-1/'))
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], participant.user)
        self.assertContains(response, 'Welcome to Session 1')

    def test_valid_form_submit_next_new_session_2(self):
        """
        Test that the facilitator can log in a participant to session 2.
        """
        participant = ParticipantFactory()
        UserPageVisit.objects.create(
            user=participant.user,
            section=self.module1,
            status='complete')

        password = generate_password(participant.user.username)
        participant.user.set_password(password)
        participant.user.save()
        response = self.client.post(
            reverse('sign-in-participant'), {
                'participant_id': participant.pk,
                'participant_location': self.location.pk,
                'participant_destination': 'next_new_session',
                'session_type': 'regular',
            }
        )

        self.assertEqual(response.status_code, 302)

        encounter = Encounter.objects.first()
        self.assertEqual(encounter.facilitator, self.u)
        self.assertEqual(encounter.participant, participant)
        self.assertEqual(encounter.location, self.location)
        self.assertEqual(encounter.session_type, 'regular')
        self.assertEqual(encounter.section, self.module2)
        self.assertEqual(encounter.section, participant.next_module_section())

        self.assertTrue(response.url.endswith('/pages/session-2/'))
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], participant.user)
        self.assertContains(response, 'Welcome to Session 2')

    def test_valid_form_submit_last_completed_activity(self):
        """
        Test that the facilitator can sign in the participant to the
        last completed activity.
        """
        participant = ParticipantFactory()
        UserPageVisit.objects.create(
            user=participant.user,
            section=self.module1,
            status='complete')

        password = generate_password(participant.user.username)
        participant.user.set_password(password)
        participant.user.save()
        response = self.client.post(
            reverse('sign-in-participant'), {
                'participant_id': participant.pk,
                'participant_location': self.location.pk,
                'participant_destination': 'last_completed_activity',
                'session_type': 'regular',
            }
        )

        self.assertEqual(response.status_code, 302)

        encounter = Encounter.objects.first()
        self.assertEqual(encounter.facilitator, self.u)
        self.assertEqual(encounter.participant, participant)
        self.assertEqual(encounter.location, self.location)
        self.assertEqual(encounter.session_type, 'regular')
        self.assertEqual(encounter.section, self.module1)
        self.assertEqual(encounter.section, participant.last_location())

        self.assertTrue(response.url.endswith('/pages/session-1/'))
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], participant.user)
        self.assertContains(response, 'Welcome to Session 1')

    def test_valid_form_submit_already_completed_session(self):
        """
        Test that the facilitator can sign in the participant to an
        already completed session.
        """
        participant = ParticipantFactory()
        UserPageVisit.objects.create(
            user=participant.user,
            section=self.module1,
            status='complete')
        UserPageVisit.objects.create(
            user=participant.user,
            section=self.module2,
            status='complete')
        UserPageVisit.objects.create(
            user=participant.user,
            section=self.module3,
            status='complete')
        UserPageVisit.objects.create(
            user=participant.user,
            section=self.module4,
            status='complete')

        password = generate_password(participant.user.username)
        participant.user.set_password(password)
        participant.user.save()
        response = self.client.post(
            reverse('sign-in-participant'), {
                'participant_id': participant.pk,
                'participant_location': self.location.pk,
                'participant_destination': 'already_completed_session',
                'already_completed_session': 3,
                'session_type': 'regular',
            }
        )

        self.assertEqual(response.status_code, 302)

        encounter = Encounter.objects.first()
        self.assertEqual(encounter.facilitator, self.u)
        self.assertEqual(encounter.participant, participant)
        self.assertEqual(encounter.location, self.location)
        self.assertEqual(encounter.session_type, 'regular')
        self.assertEqual(encounter.section, self.module3)

        self.assertTrue(response.url.endswith('/pages/session-3/'))
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], participant.user)
        self.assertContains(response, 'Welcome to Session 3')

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
                'pageblocks': [{
                    'block_type': 'Goal Setting Block',
                }],
                'children': [],
            })

    def test_get_session_1(self):
        session_num = 1
        response = self.client.get(
            reverse('participant-journal',
                    args=(self.participant.pk, session_num)))

        self.assertEqual(response.status_code, 200)

    def test_get_session_2(self):
        session_num = 2
        response = self.client.get(
            reverse('participant-journal',
                    args=(self.participant.pk, session_num)))

        self.assertEqual(response.status_code, 200)

    def test_get_session_3(self):
        session_num = 3
        response = self.client.get(
            reverse('participant-journal',
                    args=(self.participant.pk, session_num)))

        self.assertEqual(response.status_code, 200)

    def test_get_session_4(self):
        session_num = 4
        response = self.client.get(
            reverse('participant-journal',
                    args=(self.participant.pk, session_num)))

        self.assertEqual(response.status_code, 200)

    def test_get_session_5(self):
        session_num = 5
        response = self.client.get(
            reverse('participant-journal',
                    args=(self.participant.pk, session_num)))

        self.assertEqual(response.status_code, 200)
