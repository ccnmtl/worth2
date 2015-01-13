import factory
from factory.fuzzy import FuzzyText

from worth2.main.tests.factories import ParticipantFactory
from worth2.ssnm.models import Supporter


class SupporterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supporter

    participant = factory.SubFactory(ParticipantFactory)
    name = FuzzyText()
