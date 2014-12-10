from django.core.exceptions import ValidationError
from django.test import TestCase

from worth2.main.tests.factories import (
    AvatarFactory, LocationFactory, ParticipantFactory
)


class AvatarTest(TestCase):
    def setUp(self):
        self.avatar = AvatarFactory()

    def test_is_valid_from_factory(self):
        self.avatar.full_clean()

    def test_unicode(self):
        self.assertEqual(str(self.avatar), self.avatar.image.url)


class LocationTest(TestCase):
    def test_is_valid_from_factory(self):
        location = LocationFactory()
        location.full_clean()


class ParticipantTest(TestCase):
    def setUp(self):
        self.participant = ParticipantFactory()

    def test_is_valid_from_factory(self):
        self.participant.full_clean()

    def test_is_invalid_with_bad_study_id(self):
        p = ParticipantFactory(study_id='666')
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_that_participant_can_have_an_image(self):
        self.participant.avatar = AvatarFactory()
