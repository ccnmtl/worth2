from django.test import TestCase
from pagetree.helpers import get_hierarchy

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
