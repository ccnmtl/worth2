from __future__ import unicode_literals

from django.test import TestCase
from pagetree.helpers import get_hierarchy
from pagetree.models import Hierarchy, Section

from worth2.main.tests.factories import UserFactory, WorthModuleFactory, \
    UserPageVisitFactory
from worth2.main.utils import (
    get_first_block_in_module, get_module_number,
    get_module_number_from_section, percent_complete_by_module,
    default_location, percent_complete_by_pages
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
            lambda b: b.block().goal_type == 'services'
        )
        self.assertEqual(block.section.slug, 'goal-setting')

        block = get_first_block_in_module(
            'goals', 'goalsettingblock', 2,
            lambda b: b.block().goal_type == 'risk reduction'
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


class ProgressUtilsTest(TestCase):
    def setUp(self):
        self.participant = UserFactory()
        WorthModuleFactory()
        self.hierarchy = Hierarchy.objects.get(name='main')
        root = self.hierarchy.get_root()
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

    def test_default_location(self):
        self.assertEqual(
            default_location().get_absolute_url(),
            self.hierarchy.get_root().get_absolute_url()
        )

    def test_percent_complete_module_empty(self):
        for i in range(5):
            self.assertEqual(
                percent_complete_by_module(self.participant, i), 0)

    def test_percent_complete_module(self):
        section1 = Section.objects.get(slug='session-1')
        UserPageVisitFactory(
            user=self.participant, section=section1)
        module1_pages = section1.get_descendants()
        for page in module1_pages:
            UserPageVisitFactory(
                user=self.participant, section=page)

        section2 = Section.objects.get(slug='session-2')
        module2_pages = section2.get_descendants()
        UserPageVisitFactory(
            user=self.participant, section=section2)
        for page in module2_pages:
            UserPageVisitFactory(
                user=self.participant, section=page)

        self.assertEqual(percent_complete_by_module(self.participant, 1), 100)
        self.assertEqual(percent_complete_by_module(self.participant, 2), 100)
        self.assertEqual(percent_complete_by_module(self.participant, 3), 0)
        self.assertEqual(percent_complete_by_module(self.participant, 4), 0)
        self.assertEqual(percent_complete_by_module(self.participant, 5), 0)

    def test_percent_complete_by_pages(self):
        pages = self.hierarchy.get_root().get_descendants()

        section1 = Section.objects.get(slug='session-1')
        UserPageVisitFactory(
            user=self.participant, section=section1)

        pct = percent_complete_by_pages(self.participant, pages)
        self.assertEqual(pct, 4)
