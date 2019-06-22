from django.test import TestCase

from worth2.main.tests.factories import UserFactory
from worth2.ssnm.models import SupporterReportColumn
from worth2.ssnm.tests.factories import SupporterFactory


class SupporterTest(TestCase):
    def setUp(self):
        self.supporter = SupporterFactory()

    def test_is_valid_from_factory(self):
        self.supporter.full_clean()


class SupporterReportColumnTest(TestCase):

    def test_description(self):
        column = SupporterReportColumn(0, 'closeness', 'single choice')
        self.assertEquals(column.description(), 'Supporter 1 Closeness')

    def test_identifier(self):
        column = SupporterReportColumn(0, 'closeness', 'single choice')
        self.assertEquals(column.identifier(), 'supporter_1_closeness')

    def test_metadata(self):
        column = SupporterReportColumn(0, 'closeness', 'single choice',
                                       'VC', 'Very Close')
        self.assertEquals(column.metadata(), ['', 'supporter_1_closeness',
                                              'Social Support Network Map',
                                              'single choice',
                                              'Supporter 1 Closeness',
                                              'VC', 'Very Close'])

    def test_user_value_no_supporters(self):
        participant = UserFactory()
        column = SupporterReportColumn(0, 'closeness', 'single choice')
        self.assertEquals(column.user_value(participant), '')
        column = SupporterReportColumn(0, 'influence', 'single choice')
        self.assertEquals(column.user_value(participant), '')
        column = SupporterReportColumn(0, 'provides_emotional_support',
                                       'string')
        self.assertEquals(column.user_value(participant), '')
        column = SupporterReportColumn(0, 'provides_practical_support',
                                       'string')
        self.assertEquals(column.user_value(participant), '')

    def test_user_value_supporters(self):
        participant = UserFactory()
        SupporterFactory(user=participant)

        column = SupporterReportColumn(0, 'closeness', 'single choice')
        self.assertEquals(column.user_value(participant), 'VC')
        column = SupporterReportColumn(0, 'influence', 'single choice')
        self.assertEquals(column.user_value(participant), 'P')
        column = SupporterReportColumn(0, 'provides_emotional_support',
                                       'string')
        self.assertFalse(column.user_value(participant))
        column = SupporterReportColumn(0, 'provides_practical_support',
                                       'string')
        self.assertFalse(column.user_value(participant), '')
