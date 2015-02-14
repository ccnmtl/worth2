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
            '%s-TOTAL_FORMS' % p: '1',
            '%s-INITIAL_FORMS' % p: '0',
            '%s-MIN_NUM_FORMS' % p: '1',
            '%s-MAX_NUM_FORMS' % p: '1000',

            '%s-0-goal' % p: option.pk,
            '%s-0-text' % p: 'test explanation',
        })

        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            GoalSettingResponse.objects.filter(user=self.u).count(),
            1)

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

            '%s-0-goal' % p: None,
            '%s-0-text' % p: None,
        })

        self.assertEqual(r.status_code, 200)
        self.assertFormError(
            r, 'form', 'goal',
            'Select a valid choice. That choice is not one of the ' +
            'available choices.')
