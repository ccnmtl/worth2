from django.template import Context
from django.test import TestCase
from pagetree.helpers import get_hierarchy
from quizblock.models import Response, Submission

from worth2.main.tests.mixins import LoggedInParticipantTestMixin
from worth2.protectivebehaviors.templatetags.quizsummary import (
    PositiveQuizResponses
)


class PositiveQuizResponsesTest(LoggedInParticipantTestMixin, TestCase):
    def setUp(self):
        super(PositiveQuizResponsesTest, self).setUp()
        self.hierarchy = get_hierarchy('main', '/pages/')
        self.root = self.hierarchy.get_root()
        self.root.add_child_section_from_dict({
            'label': 'Section 1',
            'slug': 'section-1',
            'pageblocks': [{
                'block_type': 'Quiz',
                'description': 'Test Quiz',
                'rhetorical': False,
                'allow_redo': True,
                'css_extra': 'protective-behaviors',
                'show_submit_state': True,
                'questions': [
                    {
                        'text': 'Question 1',
                        'question_type': 'single choice',
                        'explanation': '',
                        'intro_text': '',
                        'answers': [
                            {
                                'value': 1,
                                'label': 'I do this.',
                                'correct': False,
                            },
                            {
                                'value': 0,
                                'label': 'I don\'t do this.',
                                'correct': False,
                            },
                        ],
                    },
                    {
                        'text': 'Question 2',
                        'question_type': 'single choice',
                        'explanation': '',
                        'intro_text': '',
                        'answers': [
                            {
                                'value': 3,
                                'label': 'I do this.',
                                'correct': False,
                            },
                            {
                                'value': 0,
                                'label': 'I don\'t do this.',
                                'correct': False,
                            },
                        ],
                    }
                ],
            }],
            'children': [],
        })
        self.quizblock = self.root.get_first_child().pageblock_set.first()
        self.question_1 = self.quizblock.block().question_set.first()
        self.question_2 = self.quizblock.block().question_set.all()[1]

    def test_basic_render(self):
        submission = Submission.objects.create(quiz=self.quizblock.block(),
                                               user=self.u)

        Response.objects.create(
            submission=submission,
            question=self.question_1,
            value='1')

        n = PositiveQuizResponses('user', 'cls', 'results')

        context = Context({
            'question': self.question_1,
            'user': self.u,
            'cls': 'protective-behaviors',
        })
        out = n.render(context)

        self.assertEqual(out, '')
        self.assertEqual(len(context['results']), 1)

    def test_render_only_shows_positive_values(self):
        submission = Submission.objects.create(quiz=self.quizblock.block(),
                                               user=self.u)
        Response.objects.create(
            submission=submission,
            question=self.question_1,
            value='1')
        Response.objects.create(
            submission=submission,
            question=self.question_2,
            value='0')

        n = PositiveQuizResponses('user', 'cls', 'results')

        context = Context({
            'question': self.question_1,
            'user': self.u,
            'cls': 'protective-behaviors',
        })
        out = n.render(context)

        self.assertEqual(out, '')
        self.assertEqual(len(context['results']), 1)

    def test_render_sorts_by_value(self):
        submission = Submission.objects.create(quiz=self.quizblock.block(),
                                               user=self.u)
        Response.objects.create(
            submission=submission,
            question=self.question_1,
            value='1')
        Response.objects.create(
            submission=submission,
            question=self.question_2,
            value='3')

        n = PositiveQuizResponses('user', 'cls', 'results')

        context = Context({
            'question': self.question_1,
            'user': self.u,
            'cls': 'protective-behaviors',
        })
        out = n.render(context)

        self.assertEqual(out, '')
        self.assertEqual(len(context['results']), 2)
        self.assertEqual(context['results'][0].question.text, 'Question 2')
        self.assertEqual(context['results'][0].value, '3')
        self.assertEqual(context['results'][1].question.text, 'Question 1')
        self.assertEqual(context['results'][1].value, '1')
