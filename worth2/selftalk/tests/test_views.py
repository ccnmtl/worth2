from django.test import TestCase
from pagetree.helpers import get_hierarchy

from worth2.main.tests.mixins import LoggedInParticipantTestMixin
from worth2.selftalk.tests.factories import (
    StatementFactory, RefutationFactory
)
from worth2.selftalk.models import StatementResponse, RefutationResponse


class StatementBlockTest(LoggedInParticipantTestMixin, TestCase):
    def setUp(self):
        super(StatementBlockTest, self).setUp()

        self.h = get_hierarchy('main', '/pages/')
        self.root = self.h.get_root()

        self.root.add_child_section_from_dict({
            'label': 'Statement Page',
            'slug': 'statement',
            'pageblocks': [{
                'block_type': 'Self-Talk Negative Statement Block',
            }],
            'children': [],
        })
        self.url = '/pages/statement/'

        self.statementblock = self.root.get_first_child().pageblock_set.first()
        assert(self.statementblock is not None)

        self.statement1 = StatementFactory()
        self.statement2 = StatementFactory()
        self.statement3 = StatementFactory()
        self.statementblock.block().statements.add(self.statement1)
        self.statementblock.block().statements.add(self.statement2)
        self.statementblock.block().statements.add(self.statement3)

        self.p = 'pageblock-%s' % self.statementblock.pk
        self.valid_post_data = {
            '%s-%d' % (self.p, self.statement1.pk): True,
            '%s-%d' % (self.p, self.statement2.pk): True,
            '%s-%d' % (self.p, self.statement3.pk): True,
        }

    def test_get(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Statement Page')

    def test_post(self):
        r = self.client.post(self.url, self.valid_post_data)

        responses = StatementResponse.objects.filter(
            statement_block=self.statementblock,
            user=self.u,
        )

        form = r.context['statement_form']
        self.assertTrue(form.is_valid())
        self.assertEqual(responses.count(), 3)

    def test_post_2(self):
        post_data = self.valid_post_data.copy()
        post_data['%s-%d' % (self.p, self.statement3.pk)] = False
        r = self.client.post(self.url, post_data)

        responses = StatementResponse.objects.filter(
            statement_block=self.statementblock,
            user=self.u,
        )

        form = r.context['statement_form']
        self.assertTrue(form.is_valid())
        self.assertEqual(responses.count(), 2)


class RefutationBlockTest(LoggedInParticipantTestMixin, TestCase):
    def setUp(self):
        super(RefutationBlockTest, self).setUp()

        self.h = get_hierarchy('main', '/pages/')
        self.root = self.h.get_root()

        self.root.add_child_section_from_dict({
            'label': 'Statement Page',
            'slug': 'statement',
            'pageblocks': [{
                'block_type': 'Self-Talk Negative Statement Block',
            }],
            'children': [],
        })
        statementblock = self.root.get_first_child().pageblock_set.first()
        assert(statementblock is not None)

        self.root.add_child_section_from_dict({
            'label': 'Refutation Page',
            'slug': 'refutation',
            'pageblocks': [{
                'block_type': 'Self-Talk Refutation Block',
                'statement_block': statementblock.block(),
            }],
            'children': [],
        })
        self.url = '/pages/refutation/'

        self.refutationblock = \
            self.root.get_first_child().get_next().pageblock_set.first()
        assert(self.refutationblock is not None)

        self.refutation1 = RefutationFactory()

        p = 'pageblock-%s' % self.refutationblock.pk
        self.valid_post_data = {
            '%s-%d' % (p, self.refutation1.pk): True,
        }

    def test_get(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Refutation Page')

    def test_post(self):
        self.client.post(self.url, self.valid_post_data)

        RefutationResponse.objects.filter(
            refutation_block=self.refutationblock.block(),
            user=self.u,
        )
