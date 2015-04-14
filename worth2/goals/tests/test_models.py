# -*- coding: utf-8 -*-

from django.test import TestCase
from pagetree.models import Hierarchy
from pagetree.tests.factories import ModuleFactory
from worth2.goals.tests.factories import (
    GoalSettingBlockFactory, GoalOptionFactory, GoalSettingResponseFactory,
    GoalCheckInBlockFactory, GoalCheckInOptionFactory,
    GoalCheckInResponseFactory
)
from worth2.main.tests.factories import (ParticipantFactory, UserFactory)


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

    def test_unicode(self):
        text = u'I will talk to a counselor or health care provider ' + \
               u'(i.e. a social worker, a counselor, a CASC, a medical ' + \
               u'doctor, etc…) about my drug or alcohol use this week'
        o = GoalOptionFactory(text=text)
        self.assertTrue(text in unicode(o))


class GoalSettingResponseTest(TestCase):
    def setUp(self):
        self.o = GoalSettingResponseFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()

    def test_unicode(self):
        text = u'I will talk to a counselor or health care provider ' + \
               u'(i.e. a social worker, a counselor, a CASC, a medical ' + \
               u'doctor, etc…) about my drug or alcohol use this week'
        o = GoalOptionFactory(text=text)
        resp = GoalSettingResponseFactory(option=o)
        self.assertTrue(text in unicode(resp))


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

    def test_unicode(self):
        text = u'I will talk to a counselor or health care provider ' + \
               u'(i.e. a social worker, a counselor, a CASC, a medical ' + \
               u'doctor, etc…) about my drug or alcohol use this week'
        o = GoalCheckInOptionFactory(text=text)
        self.assertTrue(text in unicode(o))


class GoalCheckInResponseTest(TestCase):
    def setUp(self):
        self.o = GoalCheckInResponseFactory()

    def test_is_valid_from_factory(self):
        self.o.full_clean()

    def test_unicode(self):
        self.assertTrue(
            self.o.goal_setting_response.user.username in unicode(self.o))


class GoalSettingColumnTest(TestCase):
    def setUp(self):
        self.block = GoalSettingBlockFactory()
        self.opt = GoalOptionFactory(text="Sample Option")
        self.opt_na = GoalOptionFactory(text="n/a")
        self.opt_other = GoalOptionFactory(text="Other")

        self.participant = ParticipantFactory().user
        self.staff = UserFactory(is_superuser=True)

        ModuleFactory("main", "/pages/")
        self.hierarchy = Hierarchy.objects.get(name='main')

    def test_identifier(self):
        pass

    def test_metadata(self):
        pass

    def test_user_value(self):
        pass
