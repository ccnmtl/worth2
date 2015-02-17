from django.test import TestCase

from worth2.goals.tests.factories import (
    GoalSettingBlockFactory, GoalOptionFactory, GoalSettingResponseFactory,
    GoalCheckInBlockFactory, GoalCheckInOptionFactory
)


class GoalSettingBlockTest(TestCase):
    def setUp(self):
        self.o = GoalSettingBlockFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()


class GoalOptionTest(TestCase):
    def setUp(self):
        self.o = GoalOptionFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()


class GoalSettingResponseTest(TestCase):
    def setUp(self):
        self.o = GoalSettingResponseFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()


class GoalCheckInBlockTest(TestCase):
    def setUp(self):
        self.o = GoalCheckInBlockFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()


class GoalCheckInOptionTest(TestCase):
    def setUp(self):
        self.o = GoalCheckInOptionFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()
