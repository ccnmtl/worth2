# -*- coding: utf-8 -*-

from django.test import TestCase

from worth2.goals.tests.factories import (
    GoalSettingBlockFactory, GoalOptionFactory, GoalSettingResponseFactory,
    GoalCheckInBlockFactory, GoalCheckInOptionFactory,
    GoalCheckInResponseFactory
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
