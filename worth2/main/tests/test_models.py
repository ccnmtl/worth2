from django.core.exceptions import ValidationError
from django.test import TestCase

from worth2.main.tests.factories import (
    AvatarFactory, VideoBlockFactory, WatchedVideoFactory,
    UserPageVisitFactory
)


class AvatarTest(TestCase):
    def setUp(self):
        self.avatar = AvatarFactory()

    def test_is_valid_from_factory(self):
        self.avatar.full_clean()

    def test_unicode(self):
        self.assertEqual(str(self.avatar), self.avatar.image.url)

    def test_clean_not_default(self):
        a = AvatarFactory(is_default=False)
        # shouldn't actually do anything...
        a.clean()

    def test_clean_is_default(self):
        a = AvatarFactory(is_default=True)
        a.clean()
        b = AvatarFactory(is_default=True)
        with self.assertRaises(ValidationError):
            b.clean()


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
