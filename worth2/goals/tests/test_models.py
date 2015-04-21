# -*- coding: utf-8 -*-

from django.test import TestCase, TransactionTestCase
from pagetree.helpers import get_hierarchy
from worth2.goals.models import GoalSettingColumn, GoalCheckInColumn
from worth2.goals.tests.factories import (
    GoalSettingBlockFactory, GoalOptionFactory, GoalSettingResponseFactory,
    GoalCheckInBlockFactory, GoalCheckInOptionFactory,
    GoalCheckInResponseFactory
)
from worth2.main.tests.factories import (ParticipantFactory)


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
        self.opt = GoalOptionFactory(text="Sample Option")
        self.opt_other = GoalOptionFactory(text="Other")

        self.participant = ParticipantFactory().user

        self.hierarchy = get_hierarchy('main', '/pages/')
        root = self.hierarchy.get_root()
        root.add_child_section_from_dict({
            'label': 'Goal Setting Section',
            'slug': 'goal-setting-section',
            'pageblocks': [{
                'block_type': 'Goal Setting Block',
            }],
            'children': [],
        })
        pageblock = root.get_first_child().pageblock_set.first()
        self.block = pageblock.content_object
        assert(self.block is not None)

    def test_identifier(self):
        column = GoalSettingColumn(self.block, 0, "option", self.opt)
        self.assertEquals(column.identifier(),
                          "%s_services_0_option" % self.block.id)

    def test_metadata(self):
        column = GoalSettingColumn(self.block, 0, "option", self.opt)
        self.assertEquals(column.metadata(),
                          ['main', column.identifier(), "Goal Setting Block",
                           "single choice", "Services 0 Option",
                           self.opt.id, "Sample Option"])

        column = GoalSettingColumn(self.block, 0, "text")
        self.assertEquals(column.metadata(),
                          ['main', column.identifier(), "Goal Setting Block",
                           "string", "Services 0 Text"])

    def test_user_value_no_responses(self):
        option = GoalSettingColumn(self.block, 0, "option")
        other_text = GoalSettingColumn(self.block, 0, "other_text")
        text = GoalSettingColumn(self.block, 0, "text")

        # no responses
        self.assertEquals(option.user_value(self.participant), '')
        self.assertEquals(other_text.user_value(self.participant), '')
        self.assertEquals(text.user_value(self.participant), '')

    def test_user_value_generic_option(self):
        option = GoalSettingColumn(self.block, 0, "option")
        other_text = GoalSettingColumn(self.block, 0, "other_text")
        text = GoalSettingColumn(self.block, 0, "text")

        # regular option selected -- text expected, no "other text" expected
        GoalSettingResponseFactory(goal_setting_block=self.block,
                                   user=self.participant, option=self.opt,
                                   text="sample response")
        self.assertEquals(option.user_value(self.participant), self.opt.id)
        self.assertEquals(other_text.user_value(self.participant), '')
        self.assertEquals(text.user_value(self.participant), "sample response")

    def test_user_value_other_option(self):
        option = GoalSettingColumn(self.block, 0, "option")
        other_text = GoalSettingColumn(self.block, 0, "other_text")
        text = GoalSettingColumn(self.block, 0, "text")

        # regular option selected -- text expected, no "other text" expected
        GoalSettingResponseFactory(goal_setting_block=self.block,
                                   user=self.participant,
                                   option=self.opt_other, other_text="random",
                                   text="sample response")
        self.assertEquals(option.user_value(self.participant),
                          self.opt_other.id)
        self.assertEquals(other_text.user_value(self.participant), "random")
        self.assertEquals(text.user_value(self.participant), "sample response")


class GoalCheckInColumnTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.participant = ParticipantFactory().user

        self.hierarchy = get_hierarchy('main', '/pages/')
        root = self.hierarchy.get_root()
        root.add_child_section_from_dict({
            'label': 'Goal Check In Section',
            'slug': 'goal-checkin-section',
            'pageblocks': [
                {'block_type': 'Goal Setting Block'},
                {'block_type': 'Goal Check In Block'}
            ],
            'children': [],
        })

        blocks = root.get_first_child().pageblock_set.all()
        self.assertEquals(blocks.count(), 2)
        goal_setting_block = blocks[0].content_object
        self.block = blocks[1].content_object
        self.block.goal_setting_block = goal_setting_block
        self.block.save()

        assert(self.block is not None)

    def test_identifier(self):
        column = GoalCheckInColumn(self.block, 0, 'progress')
        self.assertEquals(column.identifier(),
                          '%s_services_0_progress' %
                          self.block.goal_setting_block.id)

    def test_metadata(self):
        column = GoalCheckInColumn(self.block, 0, 'progress', 'yes', 'Yes')
        self.assertEquals(
            column.metadata(), [
                u'main',
                u'%d_services_0_progress' % self.block.goal_setting_block.id,
                'Goal Check In Block', 'single choice',
                u'Services 0 Checkin Progress', 'yes', 'Yes'
            ])
        column = GoalCheckInColumn(self.block, 0, 'other')
        self.assertEquals(column.metadata(), [
            u'main', u'%d_services_0_other' % self.block.goal_setting_block.id,
            'Goal Check In Block', 'string',
            u'Services 0 Checkin Other'
        ])

    def test_user_values_no_responses(self):
        GoalCheckInColumn(self.block, 0, 'progress')
        GoalCheckInColumn(self.block, 0, 'barrier')
        GoalCheckInColumn(self.block, 0, 'other')

    def test_i_did_it(self):
        response = GoalSettingResponseFactory(
            goal_setting_block=self.block.goal_setting_block,
            user=self.participant, text='sample')
        GoalCheckInResponseFactory(goal_setting_response=response,
                                   i_will_do_this='yes',
                                   what_got_in_the_way=None, other='')

        col = GoalCheckInColumn(self.block, 0, 'progress')
        self.assertEquals(col.user_value(self.participant), 'yes')
        col = GoalCheckInColumn(self.block, 0, 'barrier')
        self.assertEquals(col.user_value(self.participant), '')
        col = GoalCheckInColumn(self.block, 0, 'other')
        self.assertEquals(col.user_value(self.participant), '')

    def test_i_havent_started(self):
        barrier = GoalCheckInOptionFactory(text='Canned')
        response = GoalSettingResponseFactory(
            goal_setting_block=self.block.goal_setting_block,
            user=self.participant, text='sample')
        GoalCheckInResponseFactory(goal_setting_response=response,
                                   i_will_do_this='no',
                                   what_got_in_the_way=barrier,
                                   other='foobar')

        col = GoalCheckInColumn(self.block, 0, 'progress')
        self.assertEquals(col.user_value(self.participant), 'no')
        col = GoalCheckInColumn(self.block, 0, 'barrier')
        self.assertEquals(col.user_value(self.participant), barrier.id)
        col = GoalCheckInColumn(self.block, 0, 'other')
        self.assertEquals(col.user_value(self.participant), 'foobar')
