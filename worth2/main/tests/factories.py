from django.core.files.uploadedfile import SimpleUploadedFile
import factory
from factory.fuzzy import FuzzyInteger, FuzzyText

from worth2.main.models import (
    Avatar, Location, Participant
)


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

    study_id = FuzzyInteger(100000000, 999999999)
    location = factory.SubFactory(LocationFactory)
