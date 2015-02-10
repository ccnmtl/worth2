from django.test import TestCase

from pagetree.helpers import get_hierarchy

from worth2.main.tests.mixins import (
    LoggedInFacilitatorTestMixin
)


class TestQuizSubmission(LoggedInFacilitatorTestMixin, TestCase):
    def setUp(self):
        super(TestQuizSubmission, self).setUp()
        self.h = get_hierarchy('main', '/pages/')
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict({
            'label': 'Section 1',
            'slug': 'section-1',
            'pageblocks': [{
                'block_type': 'quiz',
                'description': 'Test Quiz',
                'rhetorical': False,
                'allow_redo': True,
                'show_submit_state': True,
                'questions': [{
                    'text': 'Test Question',
                    'question_type': 'single choice',
                }],
            }],
            'children': [],
        })

    def test_submit_empty_quiz(self):
        r = self.client.get('/pages/section-1/')
        self.assertEqual(r.status_code, 200)
        # FIXME
        # self.assertContains(r, 'Test Question')

        r = self.client.post('/pages/section-1/', {}, follow=True)
        self.assertRedirects(r, '/pages/section-1/')
        # FIXME
        # self.assertContains(r, 'Oops!')

    def test_submit_quiz(self):
        r = self.client.get('/pages/edit/section-1/')
        self.assertEqual(r.status_code, 200)
