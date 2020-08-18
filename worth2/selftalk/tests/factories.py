import factory
from factory.fuzzy import FuzzyText

from worth2.selftalk.models import (
    Statement, Refutation,
    StatementBlock, RefutationBlock,
    StatementResponse, RefutationResponse
)
from worth2.main.tests.factories import UserFactory


class StatementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Statement

    text = FuzzyText()


class RefutationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Refutation

    statement = factory.SubFactory(StatementFactory)
    text = FuzzyText()


class ExternalStatementBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StatementBlock

    is_internal = False
    subject_name = 'Jane'

    @factory.post_generation
    def statements(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for statement in extracted:
                self.statements.add(statement)


class InternalStatementBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StatementBlock

    is_internal = True

    @factory.post_generation
    def statements(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for statement in extracted:
                self.statements.add(statement)


class ExternalRefutationBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RefutationBlock

    statement_block = factory.SubFactory(ExternalStatementBlockFactory)


class InternalRefutationBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RefutationBlock

    statement_block = factory.SubFactory(InternalStatementBlockFactory)


class StatementResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StatementResponse

    statement = factory.SubFactory(StatementFactory)
    statement_block = factory.SubFactory(InternalStatementBlockFactory)
    user = factory.SubFactory(UserFactory)


class RefutationResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RefutationResponse

    refutation = factory.SubFactory(RefutationFactory)
    statement = factory.SubFactory(StatementFactory)
    refutation_block = factory.SubFactory(InternalRefutationBlockFactory)
    user = factory.SubFactory(UserFactory)
