from django.test import TestCase

from worth2.ssnm.tests.factories import SupporterFactory


class SupporterTest(TestCase):
    def setUp(self):
        self.supporter = SupporterFactory()

    def test_is_valid_from_factory(self):
        self.supporter.full_clean()
