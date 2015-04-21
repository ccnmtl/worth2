from django.test import TestCase
from pagetree.helpers import get_hierarchy

from worth2.main.utils import (
    get_first_block_in_module, get_module_number,
    get_module_number_from_section, get_verbose_section_name
)


class UtilsTest(TestCase):
    def setUp(self):
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

    def test_get_first_block_in_module(self):
        block = get_first_block_in_module('goals', 'goalsettingblock', 1)
        self.assertEqual(block, None)

        block = get_first_block_in_module('goals', 'goalsettingblock', 2)
        self.assertEqual(block.section.slug, 'goal-setting')

        block = get_first_block_in_module(
            'goals', 'goalsettingblock', 2,
            lambda (b): b.block().goal_type == 'services'
        )
        self.assertEqual(block.section.slug, 'goal-setting')

        block = get_first_block_in_module(
            'goals', 'goalsettingblock', 2,
            lambda (b): b.block().goal_type == 'risk reduction'
        )
        self.assertEqual(block, None)

    def test_get_module_number(self):
        avatarblock = get_first_block_in_module(
            'main', 'avatarselectorblock', 1)
        self.assertEqual(get_module_number(avatarblock), 1)
        goalsettingblock = get_first_block_in_module(
            'goals', 'goalsettingblock', 2)
        self.assertEqual(get_module_number(goalsettingblock), 2)

    def test_get_module_number_from_section(self):
        avatarblock = get_first_block_in_module(
            'main', 'avatarselectorblock', 1)
        self.assertEqual(get_module_number_from_section(
            avatarblock.section), 1)
        goalsettingblock = get_first_block_in_module(
            'goals', 'goalsettingblock', 2)
        self.assertEqual(get_module_number_from_section(
            goalsettingblock.section), 2)

    def test_get_verbose_section_name(self):
        avatarblock = get_first_block_in_module(
            'main', 'avatarselectorblock', 1)
        self.assertEqual(
            get_verbose_section_name(avatarblock.section).lower(),
            'Session 1 [Session 1]'.lower())

        goalsettingblock = get_first_block_in_module(
            'goals', 'goalsettingblock', 2)
        self.assertEqual(
            get_verbose_section_name(goalsettingblock.section).lower(),
            'Goal Setting Block page [Session 2]'.lower())
