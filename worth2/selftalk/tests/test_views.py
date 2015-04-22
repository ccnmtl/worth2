from django.test import TestCase
from pagetree.helpers import get_hierarchy

from worth2.main.tests.mixins import LoggedInParticipantTestMixin
from worth2.selftalk.tests.factories import (
    StatementFactory, StatementResponseFactory, RefutationFactory
)
from worth2.selftalk.models import (
    StatementBlock, RefutationBlock,
    StatementResponse, RefutationResponse
)


class ExternalStatementBlockTest(LoggedInParticipantTestMixin, TestCase):
    def setUp(self):
        super(ExternalStatementBlockTest, self).setUp()

        self.h = get_hierarchy('main', '/pages/')
        self.root = self.h.get_root()

        self.root.add_child_section_from_dict({
            'label': 'Statement Page',
            'slug': 'statement',
            'pageblocks': [{
                'block_type': 'Self-Talk Negative Statement Block',
                'is_internal': False,
            }],
            'children': [],
        })
        self.url = '/pages/statement/'

        self.statementblock = StatementBlock.objects.first()
        assert(self.statementblock is not None)

        self.statement1 = StatementFactory()
        self.statement2 = StatementFactory()
        self.statement3 = StatementFactory()
        self.statementblock.statements.add(self.statement1)
        self.statementblock.statements.add(self.statement2)
        self.statementblock.statements.add(self.statement3)

        self.p = 'pageblock-%s' % self.statementblock.pageblock().pk
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

        self.assertTrue(r.context['needs_submit'])
        self.assertTrue(r.context['is_submitted'])
        self.assertTrue(r.context['allow_redo'])
        self.assertContains(r, 'I want to change my answers.')

        r = self.client.get(self.url)
        self.assertTrue(r.context['needs_submit'])
        self.assertTrue(r.context['is_submitted'])
        self.assertTrue(r.context['allow_redo'])
        self.assertContains(r, 'I want to change my answers.')

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


class ExternalRefutationBlockTest(LoggedInParticipantTestMixin, TestCase):
    def setUp(self):
        super(ExternalRefutationBlockTest, self).setUp()

        self.h = get_hierarchy('main', '/pages/')
        self.root = self.h.get_root()

        self.root.add_child_section_from_dict({
            'label': 'Statement Page',
            'slug': 'statement',
            'pageblocks': [{
                'block_type': 'Self-Talk Negative Statement Block',
                'is_internal': False,
            }],
            'children': [],
        })
        self.statementblock = StatementBlock.objects.first()
        assert(self.statementblock is not None)

        self.statement1 = StatementFactory()
        self.statement2 = StatementFactory()
        self.statement3 = StatementFactory()

        self.statementblock.statements.add(self.statement1)
        self.statementblock.statements.add(self.statement2)
        self.statementblock.statements.add(self.statement3)

        self.statementresponse1 = StatementResponseFactory(
            user=self.u,
            statement_block=self.statementblock,
            statement=self.statement1)
        self.statementresponse2 = StatementResponseFactory(
            user=self.u,
            statement_block=self.statementblock,
            statement=self.statement2)
        self.statementresponse3 = StatementResponseFactory(
            user=self.u,
            statement_block=self.statementblock,
            statement=self.statement3)

        self.root.add_child_section_from_dict({
            'label': 'Refutation Page',
            'slug': 'refutation',
            'pageblocks': [{
                'block_type': 'Self-Talk Refutation Block',
                'statement_block': self.statementblock,
            }],
            'children': [],
        })
        self.url = '/pages/refutation/'

        self.refutationblock = RefutationBlock.objects.first()
        assert(self.refutationblock is not None)

        # Create 3 refutations for each negative statement
        self.refutation1 = RefutationFactory(statement=self.statement1)
        self.refutation2 = RefutationFactory(statement=self.statement1)
        self.refutation3 = RefutationFactory(statement=self.statement1)
        self.refutation4 = RefutationFactory(statement=self.statement2)
        self.refutation5 = RefutationFactory(statement=self.statement2)
        self.refutation6 = RefutationFactory(statement=self.statement2)
        self.refutation7 = RefutationFactory(statement=self.statement3)
        self.refutation8 = RefutationFactory(statement=self.statement3)
        self.refutation9 = RefutationFactory(statement=self.statement3)

        self.p = 'pageblock-%s' % self.refutationblock.pageblock().pk
        self.valid_post_data = {
            '%s-refutation-%d' % (
                self.p, self.statement1.pk): self.refutation1.pk,
            '%s-refutation-%d' % (
                self.p, self.statement2.pk): self.refutation4.pk,
            '%s-refutation-%d' % (
                self.p, self.statement3.pk): self.refutation7.pk,
        }

    def test_get(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Refutation Page')

    def test_post(self):
        r = self.client.post(self.url, self.valid_post_data)

        responses = RefutationResponse.objects.filter(
            refutation_block=self.refutationblock,
            user=self.u,
        )
        form = r.context['refutation_form']

        self.assertTrue(form.is_valid())
        self.assertEqual(responses.count(), 3)

        self.assertEqual(
            RefutationResponse.objects.filter(
                refutation_block=self.refutationblock,
                user=self.u,
                refutation=self.refutation1
            ).count(), 1)
        self.assertEqual(
            RefutationResponse.objects.filter(
                refutation_block=self.refutationblock,
                user=self.u,
                refutation=self.refutation4
            ).count(), 1)
        self.assertEqual(
            RefutationResponse.objects.filter(
                refutation_block=self.refutationblock,
                user=self.u,
                refutation=self.refutation7
            ).count(), 1)

        self.assertTrue(r.context['needs_submit'])
        self.assertTrue(r.context['is_submitted'])
        self.assertTrue(r.context['allow_redo'])
        self.assertContains(r, 'I want to change my answers.')

        r = self.client.get(self.url)
        self.assertContains(r, self.refutation1.text)
        self.assertContains(r, self.refutation4.text)
        self.assertContains(r, self.refutation7.text)
        self.assertTrue(r.context['needs_submit'])
        self.assertTrue(r.context['is_submitted'])
        self.assertTrue(r.context['allow_redo'])
        self.assertContains(r, 'I want to change my answers.')

    def test_post_with_other_option(self):
        refutation_other = RefutationFactory(statement=self.statement1,
                                             text='Other')
        post_data = self.valid_post_data.copy()
        post_data['%s-refutation-%d' % (
            self.p, self.statement1.pk)] = refutation_other.pk
        post_data['%s-other-%d' % (
            self.p, self.statement1.pk)] = 'Testing other text'

        r = self.client.post(self.url, post_data)

        responses = RefutationResponse.objects.filter(
            refutation_block=self.refutationblock,
            user=self.u,
        )
        form = r.context['refutation_form']

        self.assertTrue(form.is_valid())
        self.assertEqual(responses.count(), 3)

        other_response = RefutationResponse.objects.get(
            refutation_block=self.refutationblock,
            refutation=refutation_other, user=self.u)
        self.assertEqual(other_response.other_text, 'Testing other text')

        r = self.client.get(self.url)
        self.assertContains(r, 'Other')


class InternalStatementBlockTest(LoggedInParticipantTestMixin, TestCase):
    def setUp(self):
        super(InternalStatementBlockTest, self).setUp()

        self.h = get_hierarchy('main', '/pages/')
        self.root = self.h.get_root()

        self.root.add_child_section_from_dict({
            'label': 'Statement Page',
            'slug': 'statement',
            'pageblocks': [{
                'block_type': 'Self-Talk Negative Statement Block',
                'is_internal': True,
            }],
            'children': [],
        })
        self.url = '/pages/statement/'

        self.statementblock = StatementBlock.objects.first()
        assert(self.statementblock is not None)

        self.statement1 = StatementFactory()
        self.statement2 = StatementFactory()
        self.statement3 = StatementFactory()
        self.statementblock.statements.add(self.statement1)
        self.statementblock.statements.add(self.statement2)
        self.statementblock.statements.add(self.statement3)

        self.p = 'pageblock-%s' % self.statementblock.pageblock().pk
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

        self.assertTrue(r.context['needs_submit'])
        self.assertTrue(r.context['is_submitted'])
        self.assertTrue(r.context['allow_redo'])
        self.assertContains(r, 'I want to change my answers.')

        r = self.client.get(self.url)
        self.assertTrue(r.context['needs_submit'])
        self.assertTrue(r.context['is_submitted'])
        self.assertTrue(r.context['allow_redo'])
        self.assertContains(r, 'I want to change my answers.')

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


class InternalRefutationBlockTest(LoggedInParticipantTestMixin, TestCase):
    def setUp(self):
        super(InternalRefutationBlockTest, self).setUp()

        self.h = get_hierarchy('main', '/pages/')
        self.root = self.h.get_root()

        self.root.add_child_section_from_dict({
            'label': 'Statement Page',
            'slug': 'statement',
            'pageblocks': [{
                'block_type': 'Self-Talk Negative Statement Block',
                'is_internal': True,
            }],
            'children': [],
        })
        self.statementblock = StatementBlock.objects.first()
        assert(self.statementblock is not None)

        self.statement1 = StatementFactory()
        self.statement2 = StatementFactory()
        self.statement3 = StatementFactory()

        self.statementblock.statements.add(self.statement1)
        self.statementblock.statements.add(self.statement2)
        self.statementblock.statements.add(self.statement3)

        self.statementresponse1 = StatementResponseFactory(
            user=self.u,
            statement_block=self.statementblock,
            statement=self.statement1)
        self.statementresponse2 = StatementResponseFactory(
            user=self.u,
            statement_block=self.statementblock,
            statement=self.statement2)
        self.statementresponse3 = StatementResponseFactory(
            user=self.u,
            statement_block=self.statementblock,
            statement=self.statement3)

        self.root.add_child_section_from_dict({
            'label': 'Refutation Page',
            'slug': 'refutation',
            'pageblocks': [{
                'block_type': 'Self-Talk Refutation Block',
                'statement_block': self.statementblock,
            }],
            'children': [],
        })
        self.url = '/pages/refutation/'

        self.refutationblock = RefutationBlock.objects.first()
        assert(self.refutationblock is not None)

        # Create 3 refutations for each negative statement
        self.refutation1 = RefutationFactory(statement=self.statement1)
        self.refutation2 = RefutationFactory(statement=self.statement1)
        self.refutation3 = RefutationFactory(statement=self.statement1)
        self.refutation4 = RefutationFactory(statement=self.statement2)
        self.refutation5 = RefutationFactory(statement=self.statement2)
        self.refutation6 = RefutationFactory(statement=self.statement2)
        self.refutation7 = RefutationFactory(statement=self.statement3)
        self.refutation8 = RefutationFactory(statement=self.statement3)
        self.refutation9 = RefutationFactory(statement=self.statement3)

        self.p = 'pageblock-%s' % self.refutationblock.pageblock().pk
        self.valid_post_data = {
            '%s-refutation-%d' % (
                self.p, self.statement1.pk): self.refutation1.pk,
            '%s-refutation-%d' % (
                self.p, self.statement2.pk): self.refutation4.pk,
            '%s-refutation-%d' % (
                self.p, self.statement3.pk): self.refutation7.pk,
        }

    def test_get(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Refutation Page')

    def test_post(self):
        r = self.client.post(self.url, self.valid_post_data)

        responses = RefutationResponse.objects.filter(
            refutation_block=self.refutationblock,
            user=self.u,
        )
        form = r.context['refutation_form']

        self.assertTrue(form.is_valid())
        self.assertEqual(responses.count(), 3)

        self.assertEqual(
            RefutationResponse.objects.filter(
                refutation_block=self.refutationblock,
                user=self.u,
                refutation=self.refutation1
            ).count(), 1)
        self.assertEqual(
            RefutationResponse.objects.filter(
                refutation_block=self.refutationblock,
                user=self.u,
                refutation=self.refutation4
            ).count(), 1)
        self.assertEqual(
            RefutationResponse.objects.filter(
                refutation_block=self.refutationblock,
                user=self.u,
                refutation=self.refutation7
            ).count(), 1)

        self.assertTrue(r.context['needs_submit'])
        self.assertTrue(r.context['is_submitted'])
        self.assertTrue(r.context['allow_redo'])
        self.assertContains(r, 'I want to change my answers.')

        r = self.client.get(self.url)
        self.assertContains(r, self.refutation1.text)
        self.assertContains(r, self.refutation4.text)
        self.assertContains(r, self.refutation7.text)
        self.assertTrue(r.context['needs_submit'])
        self.assertTrue(r.context['is_submitted'])
        self.assertTrue(r.context['allow_redo'])
        self.assertContains(r, 'I want to change my answers.')

    def test_post_with_other_option(self):
        refutation_other = RefutationFactory(statement=self.statement1,
                                             text='Other')
        post_data = self.valid_post_data.copy()
        post_data['%s-refutation-%d' % (
            self.p, self.statement1.pk)] = refutation_other.pk
        post_data['%s-other-%d' % (
            self.p, self.statement1.pk)] = 'Testing other text'

        r = self.client.post(self.url, post_data)

        responses = RefutationResponse.objects.filter(
            refutation_block=self.refutationblock,
            user=self.u,
        )
        form = r.context['refutation_form']

        self.assertTrue(form.is_valid())
        self.assertEqual(responses.count(), 3)

        other_response = RefutationResponse.objects.get(
            refutation_block=self.refutationblock,
            refutation=refutation_other, user=self.u)
        self.assertEqual(other_response.other_text, 'Testing other text')

        r = self.client.get(self.url)
        self.assertContains(r, 'Other')
