from django.test import TestCase
from django.urls import reverse
from pagetree.helpers import get_hierarchy

from worth2.main.models import Participant
from worth2.main.tests.factories import (
    AvatarFactory, ParticipantFactory, UserFactory)
from worth2.main.tests.mixins import (
    LoggedInFacilitatorTestMixin, LoggedInParticipantTestMixin,
    LoggedInSuperuserTestMixin
)


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
        response = self.client.get('/')
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
        self.assertEqual(len(response.context['active_participants']), 0)
        self.assertEqual(len(response.context['cohorts']), 0)


class ManageParticipantsUnAuthedTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('manage-participants'))
        self.assertEqual(response.status_code, 302)


class JournalsTest(TestCase):
    def setUp(self):
        self.participant = UserFactory()
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
        self.client.login(username=self.participant.username, password='test')

    def test_get_sessions(self):
        for i in range(1, 6):
            response = self.client.get(reverse('journal', args=[i]))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Session {}'.format(i))


class ArchiveParticipantTest(LoggedInFacilitatorTestMixin, TestCase):
    def setUp(self):
        super(ArchiveParticipantTest, self).setUp()
        self.participant = ParticipantFactory()

    def test_get(self):
        response = self.client.get(
            reverse('archive-participant', args=(self.participant.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.assertFalse(self.participant.is_archived)
        response = self.client.post(
            reverse('archive-participant', args=(self.participant.pk,)))
        self.participant.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.participant.is_archived)
