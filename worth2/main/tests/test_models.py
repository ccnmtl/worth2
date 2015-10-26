from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from pagetree.models import Hierarchy, Section

from worth2.main.models import Participant
from worth2.main.tests.factories import (
    AvatarFactory, EncounterFactory, LocationFactory, ParticipantFactory,
    VideoBlockFactory, WatchedVideoFactory, UserPageVisitFactory,
    WorthModuleFactory
)


class AvatarTest(TestCase):
    def setUp(self):
        self.avatar = AvatarFactory()

    def test_is_valid_from_factory(self):
        self.avatar.full_clean()

    def test_unicode(self):
        self.assertEqual(str(self.avatar), self.avatar.image.url)


class EncounterTest(TestCase):
    def setUp(self):
        self.encounter = EncounterFactory()

    def test_is_valid_from_factory(self):
        self.encounter.full_clean()


class LocationTest(TestCase):
    def test_is_valid_from_factory(self):
        location = LocationFactory()
        location.full_clean()


class ParticipantTest(TestCase):
    def setUp(self):
        self.participant = ParticipantFactory()
        WorthModuleFactory()
        self.hierarchy = Hierarchy.objects.get(name='main')
        root = self.hierarchy.get_root()
        root.add_child_section_from_dict({
            'label': 'Session 1',
            'slug': 'session-1',
            'pageblocks': [{
                'block_type': 'Avatar Selector Block',
            }],
            'children': [],
        })
        root.add_child_section_from_dict({
            'label': 'Session 2',
            'slug': 'session-2',
            'pageblocks': [],
            'children': [{
                'label': 'Goal Setting Block page',
                'slug': 'goal-setting',
                'pageblocks': [{
                    'block_type': 'Goal Setting Block',
                }]
            }],
        })

    def test_is_valid_from_factory(self):
        self.participant.full_clean()

    def test_is_invalid_with_bad_study_id(self):
        p = ParticipantFactory(study_id='666')
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_that_participant_can_have_an_image(self):
        self.participant.avatar = AvatarFactory()

    def test_default_location(self):
        self.assertEqual(
            self.participant.default_location().get_absolute_url(),
            self.hierarchy.get_root().get_absolute_url()
        )

    def test_highest_module_accessed(self):
        self.assertEqual(
            self.participant.highest_module_accessed(), -1)

        section1 = Section.objects.get(slug='session-1')
        upv1 = UserPageVisitFactory(
            user=self.participant.user, section=section1)
        self.assertEqual(
            self.participant.highest_module_accessed(), 1)

        section2 = Section.objects.get(slug='session-2')
        goalsection = Section.objects.get(slug='goal-setting')
        UserPageVisitFactory(user=self.participant.user, section=section2)
        UserPageVisitFactory(user=self.participant.user, section=goalsection)
        self.assertEqual(
            self.participant.highest_module_accessed(), 2)

        upv1.last_visit = datetime.now()
        upv1.save()
        self.assertEqual(
            self.participant.highest_module_accessed(), 2)

    def test_highest_module_accessed2(self):
        section1 = Section.objects.get(slug='session-1')
        upv1 = UserPageVisitFactory(
            user=self.participant.user, section=section1)
        Section.objects.get(slug='session-2')
        goalsection = Section.objects.get(slug='goal-setting')
        UserPageVisitFactory(user=self.participant.user, section=goalsection)
        self.assertEqual(
            self.participant.highest_module_accessed(), 2)

        upv1.last_visit = datetime.now()
        upv1.save()
        self.assertEqual(
            self.participant.highest_module_accessed(), 2)

    def test_next_module(self):
        self.assertEqual(
            self.participant.next_module(), 1,
            'Newly created participants have next_module set to 1')

        section1 = Section.objects.get(slug='session-1')
        upv1 = UserPageVisitFactory(
            user=self.participant.user, section=section1)
        self.assertEqual(self.participant.next_module(), 2)

        section2 = Section.objects.get(slug='session-2')
        goalsection = Section.objects.get(slug='goal-setting')
        UserPageVisitFactory(user=self.participant.user, section=section2)
        UserPageVisitFactory(user=self.participant.user, section=goalsection)
        self.assertEqual(self.participant.next_module(), 3)

        upv1.last_visit = datetime.now()
        upv1.save()
        self.assertEqual(self.participant.next_module(), 3)

    def test_percent_complete_module_empty(self):
        for i in range(5):
            self.assertEqual(
                self.participant.percent_complete_module(i), 0)

    def test_percent_complete_module(self):
        section1 = Section.objects.get(slug='session-1')
        UserPageVisitFactory(
            user=self.participant.user, section=section1)
        module1_pages = section1.get_descendants()
        for page in module1_pages:
            UserPageVisitFactory(
                user=self.participant.user, section=page)

        section2 = Section.objects.get(slug='session-2')
        module2_pages = section2.get_descendants()
        UserPageVisitFactory(
            user=self.participant.user, section=section2)
        for page in module2_pages:
            UserPageVisitFactory(
                user=self.participant.user, section=page)

        self.assertEqual(
            self.participant.percent_complete_module(1), 100)
        self.assertEqual(
            self.participant.percent_complete_module(2), 100)
        self.assertEqual(
            self.participant.percent_complete_module(3), 0)
        self.assertEqual(
            self.participant.percent_complete_module(4), 0)
        self.assertEqual(
            self.participant.percent_complete_module(5), 0)


class ParticipantManagerTest(TestCase):
    def test_cohort_ids_empty(self):
        self.assertEqual(Participant.objects.cohort_ids(), [])

    def test_cohort_ids_removes_null(self):
        ParticipantFactory()
        ParticipantFactory()
        ParticipantFactory()
        self.assertEqual(Participant.objects.cohort_ids(), [])

    def test_cohort_ids_are_sorted(self):
        ParticipantFactory(cohort_id='111')
        ParticipantFactory(cohort_id='333')
        ParticipantFactory(cohort_id='222')
        self.assertEqual(
            Participant.objects.cohort_ids(),
            ['111', '222', '333']
        )

    def test_cohort_ids_removes_duplicates(self):
        ParticipantFactory(cohort_id='111')
        ParticipantFactory(cohort_id='333')
        ParticipantFactory(cohort_id='222')
        ParticipantFactory(cohort_id='222')
        ParticipantFactory(cohort_id='222')
        ParticipantFactory(cohort_id='333')
        ParticipantFactory(cohort_id='333')
        ParticipantFactory(cohort_id='333')
        ParticipantFactory(cohort_id='222')
        self.assertEqual(
            Participant.objects.cohort_ids(),
            ['111', '222', '333']
        )


class VideoBlockTest(TestCase):
    def setUp(self):
        self.video_block = VideoBlockFactory()

    def test_is_valid_from_factory(self):
        self.video_block.full_clean()


class WatchedVideoTest(TestCase):
    def setUp(self):
        self.watched_video = WatchedVideoFactory()

    def test_is_valid_from_factory(self):
        self.watched_video.full_clean()


class UserPageVisitFactoryTest(TestCase):
    def setUp(self):
        self.upv = UserPageVisitFactory()

    def test_is_valid_from_factory(self):
        self.upv.full_clean()
