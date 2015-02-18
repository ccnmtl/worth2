import factory
from factory.fuzzy import FuzzyText

from worth2.main.tests.factories import UserFactory
from worth2.ssnm.models import Supporter


class SupporterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supporter

    user = factory.SubFactory(UserFactory)
    name = FuzzyText()
