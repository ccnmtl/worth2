from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import factory
from factory.fuzzy import FuzzyText
from pagetree.tests.factories import RootSectionFactory
from pagetree.models import UserPageVisit

from worth2.main.auth import generate_password
from worth2.main.models import (
    Avatar, Encounter, Location, Participant, VideoBlock, WatchedVideo
)


class InactiveUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = FuzzyText()
    password = factory.LazyAttribute(lambda u: generate_password(u.username))
    is_active = False


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = FuzzyText()
    password = factory.PostGenerationMethodCall('set_password', 'test')


class AvatarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Avatar

    image = SimpleUploadedFile('test.png', '')


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    name = FuzzyText()


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Participant

    user = factory.SubFactory(InactiveUserFactory)
    first_location = factory.SubFactory(LocationFactory)
    location = factory.SubFactory(LocationFactory)
    study_id = FuzzyText(length=12, chars='1234567890')
    is_archived = False


class EncounterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Encounter

    facilitator = factory.SubFactory(UserFactory)
    participant = factory.SubFactory(ParticipantFactory)
    location = factory.SubFactory(LocationFactory)
    section = factory.SubFactory(RootSectionFactory)


class VideoBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VideoBlock

    video_id = FuzzyText()


class WatchedVideoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WatchedVideo

    user = factory.SubFactory(UserFactory)
    video_id = FuzzyText()


# TODO: Move this to django-pagetree
class UserPageVisitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserPageVisit

    user = factory.SubFactory(UserFactory)
    section = factory.SubFactory(RootSectionFactory)
