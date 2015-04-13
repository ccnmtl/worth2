from django.core.exceptions import ValidationError
from django.test import TestCase
from pagetree.models import Hierarchy
from pagetree.tests.factories import ModuleFactory

from worth2.main.models import Participant
from worth2.main.tests.factories import (
    AvatarFactory, EncounterFactory, LocationFactory, ParticipantFactory,
    VideoBlockFactory, WatchedVideoFactory
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
        ModuleFactory('main', 'main')
        self.hierarchy = Hierarchy.objects.get(name='main')

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

    def test_last_session_accessed(self):
        r = self.participant.last_session_accessed(
            '/pages/session-1/some-activity')
        self.assertEqual(r, 1)
        r = self.participant.last_session_accessed(
            '/pages/session-1/')
        self.assertEqual(r, 1)

        r = self.participant.last_session_accessed(
            '/pages/session-5/session-5-activity')
        self.assertEqual(r, 5)

    def test_verbose_section_name(self):
        s = self.participant.verbose_section_name(
            self.participant.last_location())
        self.assertEqual(s, 'Root')

    def test_last_location_verbose(self):
        s = self.participant.last_location_verbose()
        self.assertEqual(s, 'Root')

    def test_next_location_verbose(self):
        s = self.participant.next_location_verbose()
        self.assertEqual(s, 'One (one)')


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
