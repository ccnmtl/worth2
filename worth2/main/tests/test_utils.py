from django.test import TestCase
from pagetree.helpers import get_hierarchy

from worth2.main.utils import get_first_block_in_session


class UtilsTest(TestCase):
    def test_get_first_block_in_session(self):
        h = get_hierarchy('main', '/pages/')
        root = h.get_root()
        root.add_child_section_from_dict({
            'label': 'Session 1',
            'slug': 'session-1',
            'pageblocks': [{
                'block_type': 'Avatar Selector Block',
            }],
            'children': [],
        })
        root.add_child_section_from_dict({
            'label': 'Session 2',
            'slug': 'session-2',
            'pageblocks': [],
            'children': [{
                'label': 'Goal Setting Block page',
                'slug': 'goal-setting',
                'pageblocks': [{
                    'block_type': 'Goal Setting Block',
                }]
            }],
        })

        block = get_first_block_in_session('goal setting block', 1)
        self.assertEqual(block, None)

        block = get_first_block_in_session('goal setting block', 2)
        self.assertEqual(block.section.slug, 'goal-setting')

        block = get_first_block_in_session(
            'goal setting block', 2,
            lambda (b): b.block().goal_type == 'services'
        )
        self.assertEqual(block.section.slug, 'goal-setting')

        block = get_first_block_in_session(
            'goal setting block', 2,
            lambda (b): b.block().goal_type == 'risk reduction'
        )
        self.assertEqual(block, None)
