from django.test import TestCase
from pagetree.helpers import get_hierarchy

from worth2.goals.tests.factories import GoalOptionFactory
from worth2.goals.models import GoalSettingResponse
from worth2.main.tests.mixins import (
    LoggedInParticipantTestMixin
)


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
        self.assertContains(r, 'My Goals')
        self.assertContains(r, 'class="goal-setting"')

    def test_post(self):
        pageblock = self.root.get_first_child().pageblock_set.first()
        option = GoalOptionFactory(goal_setting_block=pageblock.block())
        p = 'pageblock-%s' % pageblock.pk
        r = self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '3',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: option.pk,
            '%s-0-text' % p: 'test explanation',
            '%s-1-option' % p: option.pk,
            '%s-1-text' % p: 'test explanation 2',
            '%s-2-option' % p: option.pk,
            '%s-2-text' % p: 'test explanation 3',
        })

        responses = GoalSettingResponse.objects.filter(
            goal_setting_block=pageblock,
            user=self.u,
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(responses.count(), 3)
        self.assertEqual(responses.first().text, 'test explanation')
        self.assertEqual(responses.all()[1].text, 'test explanation 2')
        self.assertEqual(responses.last().text, 'test explanation 3')

    def test_post_multiple_times(self):
        """
        Assert that updating the first form in the formset multiple
        times doesn't create multiple responses for it.
        """

        pageblock = self.root.get_first_child().pageblock_set.first()
        option = GoalOptionFactory(goal_setting_block=pageblock.block())
        option2 = GoalOptionFactory(goal_setting_block=pageblock.block())

        p = 'pageblock-%s' % pageblock.pk
        self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: option.pk,
            '%s-0-text' % p: 'test explanation',
        })

        self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: option2.pk,
            '%s-0-text' % p: 'test explanation 2',
        })

        r = self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: option.pk,
            '%s-0-text' % p: 'test explanation 3',
        })

        self.assertEqual(r.status_code, 302)
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
        GoalOptionFactory(goal_setting_block=pageblock.block())
        p = 'pageblock-%s' % pageblock.pk
        r = self.client.post(self.url, {
            # Formset Management form params
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-option' % p: None,
            '%s-0-text' % p: None,
        })

        self.assertEqual(r.status_code, 200)
        self.assertFormError(
            r, 'form', 'option',
            'Select a valid choice. That choice is not one of the ' +
            'available choices.')
