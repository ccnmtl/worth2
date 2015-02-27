from django.test import TestCase

from worth2.selftalk.tests.factories import (
    StatementFactory, RefutationFactory,
    ExternalStatementBlockFactory, InternalStatementBlockFactory,
    ExternalRefutationBlockFactory, InternalRefutationBlockFactory,
    StatementResponseFactory, RefutationResponseFactory
)


class StatemetnTest(TestCase):
    def setUp(self):
        self.o = StatementFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()


class RefutationTest(TestCase):
    def setUp(self):
        self.o = RefutationFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()


class ExternalStatementBlockTest(TestCase):
    def setUp(self):
        self.o = ExternalStatementBlockFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()


class InternalStatementBlockTest(TestCase):
    def setUp(self):
        self.o = InternalStatementBlockFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()


class ExternalRefutationBlockTest(TestCase):
    def setUp(self):
        self.o = ExternalRefutationBlockFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()


class InternalRefutationBlockTest(TestCase):
    def setUp(self):
        self.o = InternalRefutationBlockFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()


class StatementResponseTest(TestCase):
    def setUp(self):
        self.o = StatementResponseFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()


class RefutationResponseTest(TestCase):
    def setUp(self):
        self.o = RefutationResponseFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()
