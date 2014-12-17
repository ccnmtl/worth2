from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import factory
from factory.fuzzy import FuzzyText

from worth2.main.models import (
    Avatar, Location, Participant
)


class InactiveUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = FuzzyText()
    is_active = False


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
    study_id = FuzzyText(prefix='7')
