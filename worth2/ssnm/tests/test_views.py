from django.test import TestCase
from pagetree.helpers import get_hierarchy

from worth2.main.tests.mixins import LoggedInUserTestMixin


class SsnmBlockTest(LoggedInUserTestMixin, TestCase):
    def setUp(self):
        super(SsnmBlockTest, self).setUp()

        self.h = get_hierarchy('main', '/pages/')
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict({
            'label': 'SSNM Section',
            'slug': 'ssnm-section',
            'pageblocks': [{
                'block_type': 'Social Support Network Map',
            }],
            'children': [],
        })
        self.url = '/pages/ssnm-section/'

    def test_get(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'SSNM Section')
        self.assertContains(r, 'My Social Support Network')
