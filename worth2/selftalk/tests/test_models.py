from __future__ import unicode_literals

from django.test import TestCase
from django.utils.encoding import smart_text

from worth2.main.tests.factories import UserFactory
from worth2.selftalk.tests.factories import (
    StatementFactory, RefutationFactory,
    ExternalStatementBlockFactory, InternalStatementBlockFactory,
    ExternalRefutationBlockFactory, InternalRefutationBlockFactory,
    StatementResponseFactory, RefutationResponseFactory
)


class StatementTest(TestCase):
    def setUp(self):
        self.o = StatementFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()

    def test_unicode(self):
        self.assertEqual(smart_text(self.o), self.o.text)


class RefutationTest(TestCase):
    def setUp(self):
        self.o = RefutationFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()

    def test_unicode(self):
        self.assertEqual(smart_text(self.o), self.o.text)


class ExternalStatementBlockTest(TestCase):
    def setUp(self):
        self.o = ExternalStatementBlockFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()

    def test_clear_user_submissions(self):
        self.o.clear_user_submissions(UserFactory())

    def test_unicode(self):
        self.assertEqual(
            str(self.o),
            "Jane's Statement Block [Session -1] id: %d" % self.o.id)
        self.o.subject_name = ""
        self.assertEqual(
            str(self.o),
            "External Statement Block [Session -1] id: %d" % self.o.id)

    def test_edit_form(self):
        self.assertIsNotNone(self.o.edit_form())


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
        self.assertEqual(self.o.subject_name,
                         self.o.statement_block.subject_name)

    def test_clear_user_submissions(self):
        self.o.clear_user_submissions(UserFactory())

    def test_unicode(self):
        self.assertEqual(
            str(self.o),
            "Self-Talk Refutation Block [-1] id: %d" % self.o.id)

    def test_edit_form(self):
        self.assertIsNotNone(self.o.edit_form())


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

    def test_unicode(self):
        self.assertEqual(smart_text(self.o), smart_text(self.o.statement))
        self.o.other_text = "something else"
        self.assertEqual(str(self.o), "something else")


class RefutationResponseTest(TestCase):
    def setUp(self):
        self.o = RefutationResponseFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()

    def test_unicode(self):
        self.assertEqual(smart_text(self.o), smart_text(self.o.refutation))
        self.o.other_text = "something else"
        self.assertEqual(str(self.o), "something else")
