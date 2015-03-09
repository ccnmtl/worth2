from django.test.testcases import TestCase
from pagetree.models import Hierarchy, UserPageVisit
from pagetree.tests.factories import ModuleFactory

from worth2.main.models import WorthRawDataReport
from worth2.main.tests.factories import ParticipantFactory, UserFactory


class WorthRawDataReportTest(TestCase):

    def setUp(self):
        super(WorthRawDataReportTest, self).setUp()

        self.participant = ParticipantFactory()
        self.participant2 = ParticipantFactory()
        self.staff = UserFactory(is_superuser=True)

        ModuleFactory("main", "/pages/")

        self.hierarchy = Hierarchy.objects.get(name='main')

        root = self.hierarchy.get_root()

        root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        root.add_child_section_from_dict(
            {
                'label': 'Section 2',
                'slug': 'section-2',
                'pageblocks': [
                    {'label': 'Welcome to your new Forest Site',
                     'css_extra': 'the-css-class',
                     'block_type': 'Test Block',
                     'body': 'You should now use the edit link to add content',
                     },
                ],
                'children': [],
            })

        sections = self.hierarchy.get_root().get_descendants()
        UserPageVisit.objects.create(user=self.participant2.user,
                                     section=sections[0],
                                     status="complete")
        UserPageVisit.objects.create(user=self.participant2.user,
                                     section=sections[1],
                                     status="complete")

        self.report = WorthRawDataReport()

    def test_get_users(self):
        self.assertEquals(len(self.report.users()), 2)

    def test_standalone_columns(self):
        rows = self.report.metadata([self.hierarchy])

        header = ['hierarchy', 'itemIdentifier', 'exercise type',
                  'itemType', 'itemText', 'answerIdentifier',
                  'answerText']
        self.assertEquals(rows.next(), header)

        self.assertEquals(rows.next(), "")

        # study id
        self.assertEquals(rows.next(), ['', 'study_id', 'profile',
                                        'string', 'Randomized Study Id'])

        # cohort id
        self.assertEquals(rows.next(), ['', 'cohort_id',
                                        'profile',
                                        'string', 'Assigned Cohort Id'])

        try:
            rows.next()
        except StopIteration:
            pass  # expected
