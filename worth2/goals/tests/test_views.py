from django.test import TestCase
from pagetree.helpers import get_hierarchy

from worth2.goals.tests.factories import (
    GoalCheckInOptionFactory, GoalCheckInResponseFactory,
    GoalOptionFactory, GoalSettingResponseFactory
)
from worth2.goals.models import (
    GoalCheckInResponse, GoalSettingBlock, GoalSettingResponse
)
from worth2.main.tests.helpers import unlock_hierarchy
from worth2.main.tests.mixins import LoggedInParticipantTestMixin


class GoalCheckInBlockTest(LoggedInParticipantTestMixin, TestCase):
    def setUp(self):
        super(GoalCheckInBlockTest, self).setUp()

        self.h = get_hierarchy('main', '/pages/')
        self.root = self.h.get_root()

        self.root.add_child_section_from_dict({
            'label': 'Goal Setting Section',
            'slug': 'goal-setting-section',
            'pageblocks': [{
                'block_type': 'Goal Setting Block',
            }],
            'children': [],
        })
        self.goalsettingblock = \
            self.root.get_first_child().pageblock_set.first()
        assert(self.goalsettingblock is not None)

        self.root.add_child_section_from_dict({
            'label': 'Goal Check In Section',
            'slug': 'goal-check-in-section',
            'pageblocks': [{
                'block_type': 'Goal Check In Block',
            }],
            'children': [],
        })
        self.goalcheckinblock = \
            self.root.get_first_child().get_next().pageblock_set.first()
        assert(self.goalcheckinblock is not None)

        # Set the check-in block's setting block to the one we just
        # created.
        self.goalcheckinblock.block().goal_setting_block = \
            self.goalsettingblock.block()
        self.goalcheckinblock.block().save()
        assert(self.goalcheckinblock.block().goal_setting_block is not None)

        unlock_hierarchy(self.root.get_first_child(), self.u)

        self.url = '/pages/goal-check-in-section/'

        opt1 = GoalOptionFactory()
        opt2 = GoalOptionFactory()
        opt3 = GoalOptionFactory()

        # This option will be hidden from the check-in formset
        opt4_na = GoalOptionFactory(text='n/a')
        self.assertEqual(GoalSettingBlock.objects.count(), 1)

        self.setting_resp1 = GoalSettingResponseFactory(
            user=self.u,
            form_id=0,
            goal_setting_block=self.goalsettingblock.block(),
            option=opt1,
        )
        self.setting_resp2 = GoalSettingResponseFactory(
            user=self.u,
            form_id=1,
            goal_setting_block=self.goalsettingblock.block(),
            option=opt2,
        )
        self.setting_resp3 = GoalSettingResponseFactory(
            user=self.u,
            form_id=2,
            goal_setting_block=self.goalsettingblock.block(),
            option=opt3,
        )
        self.setting_resp4 = GoalSettingResponseFactory(
            user=self.u,
            form_id=3,
            goal_setting_block=self.goalsettingblock.block(),
            option=opt4_na,
        )
        self.setting_responses = [
            self.setting_resp1, self.setting_resp2, self.setting_resp3,
            self.setting_resp4
        ]
        self.assertEqual(GoalSettingBlock.objects.count(), 1)

        self.checkin_opt1 = GoalCheckInOptionFactory()
        self.checkin_opt2 = GoalCheckInOptionFactory()
        self.checkin_opt3 = GoalCheckInOptionFactory()
        self.checkin_opt_other = GoalCheckInOptionFactory(text='Other')

        p = 'pageblock-%s' % self.goalcheckinblock.pk
        self.valid_post_data = {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '4',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '3',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-goal_setting_response_id' % p: self.setting_resp1.pk,
            '%s-0-i_will_do_this' % p: 'yes',
            '%s-0-what_got_in_the_way' % p: self.checkin_opt2.pk,
            '%s-0-other' % p: 'form 1',

            '%s-1-goal_setting_response_id' % p: self.setting_resp2.pk,
            '%s-1-i_will_do_this' % p: 'no',
            '%s-1-what_got_in_the_way' % p: self.checkin_opt1.pk,
            '%s-1-other' % p: 'form 2',

            '%s-2-goal_setting_response_id' % p: self.setting_resp3.pk,
            '%s-2-i_will_do_this' % p: 'in progress',
            '%s-2-what_got_in_the_way' % p: self.checkin_opt3.pk,
            '%s-2-other' % p: 'form 3',
        }

    def test_get(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['checkin_formset'].forms), 4)
        self.assertContains(r, 'Goal Check In Section')
        self.assertContains(r, 'Here\'s what you committed to do')
        self.assertContains(r, 'class="goal-check-in"')

    def test_post(self):
        r = self.client.post(self.url, self.valid_post_data)

        responses = GoalCheckInResponse.objects.filter(
            goal_setting_response__in=self.setting_responses,
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(responses.count(), 3)

        self.assertEqual(responses.first().what_got_in_the_way,
                         self.checkin_opt2)
        self.assertEqual(responses.all()[1].what_got_in_the_way,
                         self.checkin_opt1)
        self.assertEqual(responses.last().what_got_in_the_way,
                         self.checkin_opt3)

        self.assertEqual(responses.first().i_will_do_this, 'yes')
        self.assertEqual(responses.all()[1].i_will_do_this, 'no')
        self.assertEqual(responses.last().i_will_do_this, 'in progress')

        self.assertEqual(responses.first().other, 'form 1')
        self.assertEqual(responses.all()[1].other, 'form 2')
        self.assertEqual(responses.last().other, 'form 3')

    def test_post_only_main_goal(self):
        """
        Assert that a submission with only the Main form populated
        doesn't validate.
        """

        p = 'pageblock-%s' % self.goalcheckinblock.pk
        r = self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '4',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '3',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-goal_setting_response_id' % p: self.setting_resp1.pk,
            '%s-0-i_will_do_this' % p: 'no',
            '%s-0-what_got_in_the_way' % p: self.checkin_opt2.pk,
            '%s-0-other' % p: 'other text for form 1',

            '%s-1-goal_setting_response_id' % p: '',
            '%s-1-i_will_do_this' % p: None,
            '%s-1-what_got_in_the_way' % p: None,
            '%s-1-other' % p: '',

            '%s-2-goal_setting_response_id' % p: '',
            '%s-2-i_will_do_this' % p: None,
            '%s-2-what_got_in_the_way' % p: None,
            '%s-2-other' % p: '',
        })

        responses = GoalCheckInResponse.objects.filter(
            goal_setting_response=self.setting_resp1,
        )

        self.assertEqual(responses.count(), 0)
        self.assertEqual(r.status_code, 200)
        self.assertFormsetError(
            r, 'checkin_formset', 1, 'i_will_do_this',
            'Select a valid choice. None is not one of the available choices.')
        self.assertFormsetError(
            r, 'checkin_formset', 2, 'i_will_do_this',
            'Select a valid choice. None is not one of the available choices.')

    def test_post_multiple_times(self):
        """
        Assert that updating the first form in the formset multiple
        times doesn't create multiple responses for it.
        """

        self.client.post(self.url, self.valid_post_data)

        p = 'pageblock-%s' % self.goalcheckinblock.pk
        new_post_data = self.valid_post_data.copy()
        new_post_data.update({
            '%s-0-other' % p: 'Updated!'
        })
        r = self.client.post(self.url, new_post_data)

        self.assertEqual(r.status_code, 200)

        responses = GoalCheckInResponse.objects.filter(
            goal_setting_response=self.setting_resp1,
        )
        self.assertEqual(responses.count(), 1)

        # Assert that the last update took effect.
        self.assertEqual(responses.first().other, 'Updated!')

    def test_post_invalid(self):
        p = 'pageblock-%s' % self.goalcheckinblock.pk
        invalid_post_data = self.valid_post_data.copy()
        invalid_post_data.update({'%s-0-i_will_do_this' % p: None})
        r = self.client.post(self.url, invalid_post_data)

        responses = GoalCheckInResponse.objects.filter(
            goal_setting_response=self.setting_resp1,
        )
        self.assertEqual(responses.count(), 0)

        self.assertEqual(r.status_code, 200)
        self.assertFormsetError(
            r, 'checkin_formset', 0, 'i_will_do_this',
            'Select a valid choice. None is not one of the available choices.')

    def test_post_i_did_it_makes_other_inputs_not_required(self):
        p = 'pageblock-%s' % self.goalcheckinblock.pk
        my_post_data = self.valid_post_data.copy()
        my_post_data.update({
            '%s-0-i_will_do_this' % p: 'yes',
            '%s-0-what_got_in_the_way' % p: '',
            '%s-0-other' % p: '',
        })
        r = self.client.post(self.url, my_post_data)

        responses = GoalCheckInResponse.objects.filter(
            goal_setting_response=self.setting_resp1,
        )
        self.assertEqual(responses.count(), 1)

        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, 'This field is required.')

    def test_post_in_progress_makes_dropdown_required(self):
        p = 'pageblock-%s' % self.goalcheckinblock.pk
        my_post_data = self.valid_post_data.copy()
        my_post_data.update({
            '%s-0-i_will_do_this' % p: 'in progress',
            '%s-0-what_got_in_the_way' % p: '',
            '%s-0-other' % p: '',
        })
        r = self.client.post(self.url, my_post_data)

        responses = GoalCheckInResponse.objects.filter(
            goal_setting_response=self.setting_resp1,
        )
        self.assertEqual(responses.count(), 0)

        self.assertEqual(r.status_code, 200)
        self.assertFormsetError(
            r, 'checkin_formset', 0, 'what_got_in_the_way',
            'This field is required.')

    def test_post_in_progress_makes_dropdown_required2(self):
        p = 'pageblock-%s' % self.goalcheckinblock.pk
        my_post_data = self.valid_post_data.copy()
        my_post_data.update({
            '%s-0-i_will_do_this' % p: 'in progress',
            '%s-0-what_got_in_the_way' % p: self.checkin_opt1.pk,
            '%s-0-other' % p: '',
        })
        r = self.client.post(self.url, my_post_data)

        responses = GoalCheckInResponse.objects.filter(
            goal_setting_response=self.setting_resp1,
        )
        self.assertEqual(responses.count(), 1)

        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, 'This field is required.')

    def test_post_other_text_is_required(self):
        p = 'pageblock-%s' % self.goalcheckinblock.pk
        my_post_data = self.valid_post_data.copy()
        my_post_data.update({
            '%s-0-i_will_do_this' % p: 'in progress',
            '%s-0-what_got_in_the_way' % p: self.checkin_opt_other.pk,
            '%s-0-other' % p: '',
        })
        r = self.client.post(self.url, my_post_data)

        responses = GoalCheckInResponse.objects.filter(
            goal_setting_response=self.setting_resp1,
        )
        self.assertEqual(responses.count(), 0)

        self.assertEqual(r.status_code, 200)
        self.assertFormsetError(
            r, 'checkin_formset', 0, 'other', 'This field is required.')

    def test_post_other_text_is_saved(self):
        p = 'pageblock-%s' % self.goalcheckinblock.pk
        my_post_data = self.valid_post_data.copy()
        my_post_data.update({
            '%s-0-i_will_do_this' % p: 'in progress',
            '%s-0-what_got_in_the_way' % p: self.checkin_opt_other.pk,
            '%s-0-other' % p: 'Some other goal',
        })
        r = self.client.post(self.url, my_post_data)

        responses = GoalCheckInResponse.objects.filter(
            goal_setting_response=self.setting_resp1,
        )
        self.assertEqual(responses.count(), 1)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(responses.first().i_will_do_this, 'in progress')
        self.assertEqual(responses.first().what_got_in_the_way,
                         self.checkin_opt_other)
        self.assertEqual(responses.first().other, 'Some other goal')

    def test_post_revising_goal_settings(self):
        """
        Test that revising goal settings for goals that already
        have associated check-ins doesn't mess up the check-in form.
        """
        # Create a checkin response corresponding to the goal setting
        # response.
        GoalCheckInResponseFactory(
            goal_setting_response=self.setting_resp1,
            i_will_do_this='yes',
        )
        self.assertEqual(
            GoalCheckInResponse.objects.filter(
                goal_setting_response=self.setting_resp1).count(),
            1)

        # POST to the goal setting response form, as if the user is
        # revising their goals.
        option = GoalOptionFactory()
        option2 = GoalOptionFactory()
        p = 'pageblock-%s' % self.goalsettingblock.pk
        goalsettingurl = '/pages/goal-setting-section/'
        self.client.post(goalsettingurl, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '3',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: option.pk,
            '%s-0-other_text' % p: '',
            '%s-0-text' % p: 'New explanation 1',
            '%s-1-other_text' % p: '',
            '%s-1-option' % p: option.pk,
            '%s-1-text' % p: 'New explanation 2',
            '%s-2-option' % p: option2.pk,
            '%s-2-other_text' % p: '',
            '%s-2-text' % p: 'New explanation 3',
        })

        # The goal setting response that the goal checkin response
        # was pointing to just changed. We need to make sure that the
        # checkin response was deleted, because it doesn't make sense
        # to keep the same checkin response for a new goal.
        self.assertEqual(
            GoalCheckInResponse.objects.filter(
                goal_setting_response=self.setting_resp1).count(),
            0)


class GoalSettingBlockTest(LoggedInParticipantTestMixin, TestCase):
    def setUp(self):
        super(GoalSettingBlockTest, self).setUp()

        self.h = get_hierarchy('main', '/pages/')
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict({
            'label': 'Goal Setting Section',
            'slug': 'goal-setting-section',
            'pageblocks': [{
                'block_type': 'Goal Setting Block',
            }],
            'children': [],
        })
        self.url = '/pages/goal-setting-section/'

    def test_get(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Goal Setting Section')
        self.assertContains(r, 'class="goal-setting"')

    def test_post(self):
        pageblock = self.root.get_first_child().pageblock_set.first()
        option = GoalOptionFactory()
        p = 'pageblock-%s' % pageblock.pk
        r = self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '3',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: option.pk,
            '%s-0-other_text' % p: '',
            '%s-0-text' % p: 'test explanation',
            '%s-1-other_text' % p: '',
            '%s-1-option' % p: option.pk,
            '%s-1-text' % p: 'test explanation 2',
            '%s-2-option' % p: option.pk,
            '%s-2-other_text' % p: '',
            '%s-2-text' % p: 'test explanation 3',
        })

        responses = GoalSettingResponse.objects.filter(
            goal_setting_block=pageblock,
            user=self.u,
        )
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '3 goals saved.')
        self.assertEqual(responses.count(), 3)
        self.assertEqual(responses.first().text, 'test explanation')
        self.assertEqual(responses.all()[1].text, 'test explanation 2')
        self.assertEqual(responses.last().text, 'test explanation 3')

    def test_post_only_main_goal(self):
        """Assert that a submission with only the Main form populated works."""

        pageblock = self.root.get_first_child().pageblock_set.first()
        option = GoalOptionFactory()
        p = 'pageblock-%s' % pageblock.pk
        r = self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '3',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: option.pk,
            '%s-0-other_text' % p: '',
            '%s-0-text' % p: 'test explanation',
        })

        responses = GoalSettingResponse.objects.filter(
            goal_setting_block=pageblock,
            user=self.u,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(responses.count(), 1)
        self.assertContains(r, '1 goal saved.')
        self.assertEqual(responses.first().option, option)
        self.assertEqual(responses.first().text, 'test explanation')

    def test_post_multiple_times(self):
        """
        Assert that updating the first form in the formset multiple
        times doesn't create multiple responses for it.
        """

        pageblock = self.root.get_first_child().pageblock_set.first()
        option = GoalOptionFactory()
        option2 = GoalOptionFactory()

        p = 'pageblock-%s' % pageblock.pk
        self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: option.pk,
            '%s-0-other_text' % p: '',
            '%s-0-text' % p: 'test explanation',
        })

        self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: option2.pk,
            '%s-0-other_text' % p: '',
            '%s-0-text' % p: 'test explanation 2',
        })

        r = self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: option.pk,
            '%s-0-other_text' % p: '',
            '%s-0-text' % p: 'test explanation 3',
        })

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '1 goal saved.')
        self.assertEqual(
            GoalSettingResponse.objects.filter(
                goal_setting_block=pageblock.block(),
                user=self.u,
            ).count(),
            1)

        goal_setting_response = GoalSettingResponse.objects.get(
            goal_setting_block=pageblock,
            user=self.u,
        )

        # Assert that the last update took effect.
        self.assertEqual(goal_setting_response.option, option)
        self.assertEqual(goal_setting_response.text, 'test explanation 3')

    def test_post_invalid(self):
        pageblock = self.root.get_first_child().pageblock_set.first()
        GoalOptionFactory()
        p = 'pageblock-%s' % pageblock.pk
        r = self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: None,
            '%s-0-other_text' % p: '',
            '%s-0-text' % p: '',
        })

        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, '1 goal saved.')
        self.assertEqual(GoalSettingResponse.objects.count(), 0)
        self.assertFormsetError(
            r, 'setting_formset', 0, 'option',
            'Select a valid choice. That choice is not one of the ' +
            'available choices.')
        self.assertFormsetError(
            r, 'setting_formset', 0, 'text',
            'This field is required.')

    def test_post_na_option_makes_text_not_required(self):
        pageblock = self.root.get_first_child().pageblock_set.first()
        GoalOptionFactory()
        na_option = GoalOptionFactory(text='n/a')
        p = 'pageblock-%s' % pageblock.pk
        r = self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: na_option.pk,
            '%s-0-other_text' % p: '',
            '%s-0-text' % p: '',
        })

        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, 'This field is required.')
        self.assertEqual(GoalSettingResponse.objects.count(), 1)
        self.assertContains(r, '1 goal saved.')

    def test_post_other_option_makes_other_text_required(self):
        pageblock = self.root.get_first_child().pageblock_set.first()
        GoalOptionFactory()
        other_option = GoalOptionFactory(text='Other')
        p = 'pageblock-%s' % pageblock.pk
        r = self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: other_option.pk,
            '%s-0-other_text' % p: '',
            '%s-0-text' % p: 'test explanation',
        })

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'This field is required.')
        self.assertNotContains(r, '1 goal saved.')
        self.assertEqual(GoalSettingResponse.objects.count(), 0)
        self.assertFormsetError(
            r, 'setting_formset', 0, 'other_text', 'This field is required.')

    def test_post_valid_with_other_option(self):
        pageblock = self.root.get_first_child().pageblock_set.first()
        GoalOptionFactory()
        other_option = GoalOptionFactory(text='Other')
        p = 'pageblock-%s' % pageblock.pk
        r = self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: other_option.pk,
            '%s-0-other_text' % p: 'Some other goal',
            '%s-0-text' % p: 'test explanation',
        })

        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, 'This field is required.')
        self.assertContains(r, '1 goal saved.')
        self.assertEqual(GoalSettingResponse.objects.count(), 1)
        response = GoalSettingResponse.objects.first()
        self.assertEqual(response.other_text, 'Some other goal')

        r = self.client.get(self.url)
        self.assertContains(r, response.other_text)
