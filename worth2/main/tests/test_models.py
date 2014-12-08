from django.test import TestCase

from worth2.main.tests.factories import (
    AvatarFactory, LocationFactory, ParticipantFactory
)


class Avatar(TestCase):
    def setUp(self):
        self.avatar = AvatarFactory()

    def test_is_valid_from_factory(self):
        AvatarFactory()

    def test_unicode(self):
        self.assertEqual(str(self.avatar), self.avatar.image.url)


class LocationTest(TestCase):
    def test_is_valid_from_factory(self):
        LocationFactory()


class ParticipantTest(TestCase):
    def setUp(self):
        self.participant = ParticipantFactory()

    def test_is_valid_from_factory(self):
        ParticipantFactory()

    def test_that_participant_can_have_an_image(self):
        self.participant.avatar = AvatarFactory()
