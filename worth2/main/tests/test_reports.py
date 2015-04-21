import datetime

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from pagetree.helpers import get_hierarchy
from pagetree.models import Hierarchy, Section, UserPageVisit
from pagetree.tests.factories import ModuleFactory

from worth2.main.reports import ParticipantReport
from worth2.main.tests.factories import (EncounterFactory, ParticipantFactory,
                                         UserFactory, LocationFactory)


class ParticipantReportTest(TestCase):

    def setUp(self):
        super(ParticipantReportTest, self).setUp()
        cache.clear()

        self.location = LocationFactory(name='Butler')

        p = ParticipantFactory(first_location=self.location,
                               location=self.location)
        self.participant = p.user

        p = ParticipantFactory(first_location=self.location,
                               location=self.location)
        self.participant2 = p.user
        self.staff = UserFactory(username='f1',
                                 first_name='Facilitator', last_name='One')

        ModuleFactory("main", "/pages/")
        self.hierarchy = Hierarchy.objects.get(name='main')
        self.report_url = reverse('participant-report')

    def test_get_users(self):
        section_one = Section.objects.get(slug='one')
        UserPageVisit.objects.create(user=self.participant,
                                     section=section_one,
                                     status="complete")
        self.assertEquals(ParticipantReport(self.hierarchy).users().count(), 1)

    def test_encounter_id(self):
        report = ParticipantReport(self.hierarchy)
        the_participant = self.participant.profile.participant
        the_participant.cohort_id = '333'
        the_participant.save()

        # modules one
        module = Section.objects.get(slug='one')
        child = Section.objects.get(slug='introduction')

        # no encounters
        self.assertIsNone(report.encounter_id(the_participant, 0, module, 0))

        # regular encounter
        e1 = EncounterFactory(participant=the_participant,
                              section=module)
        # makeup encounter
        e2 = EncounterFactory(participant=the_participant,
                              section=child, session_type='makeup')

        eid = report.encounter_id(the_participant, 0, module, 0)
        self.assertEquals(eid[0:4], '333-')
        self.assertEquals(eid[4:6], '1-')  # module index
        self.assertEquals(int(eid[6:11]), e1.facilitator.id)
        self.assertEquals(eid[12:22], e1.created_at.strftime("%y%m%d%I%M"))
        self.assertEquals(eid[22:25], '-0-')
        self.assertEquals(int(eid[25:27]), e1.location.id)

        # makeup encounter
        eid = report.encounter_id(the_participant, 0, module, 1)
        self.assertEquals(eid[0:4], '333-')
        self.assertEquals(eid[4:6], '1-')  # module index
        self.assertEquals(int(eid[6:11]), e2.facilitator.id)
        self.assertEquals(eid[12:22], e2.created_at.strftime("%y%m%d%I%M"))
        self.assertEquals(eid[22:25], '-1-')
        self.assertEquals(int(eid[25:27]), e2.location.id)

        self.assertIsNone(report.encounter_id(the_participant, 0, module, 2))

    def test_percent_complete(self):
        report = ParticipantReport(self.hierarchy)
        root = self.hierarchy.get_root()

        pct = report.percent_complete(self.participant, root)
        self.assertEquals(pct, 0)

        # visit section one & child one
        section_one = Section.objects.get(slug='one')
        child_one = Section.objects.get(slug='introduction')
        UserPageVisit.objects.create(
            user=self.participant, section=section_one, status="complete")
        UserPageVisit.objects.create(
            user=self.participant, section=child_one, status="complete")
        pct = report.percent_complete(self.participant, root)
        self.assertAlmostEquals(pct, 50.0)

        # corner case, no descendants
        hierarchy = get_hierarchy('foo')
        pct = report.percent_complete(self.participant, hierarchy.get_root())
        self.assertAlmostEquals(pct, 0)

    def test_modules_completed(self):
        report = ParticipantReport(self.hierarchy)
        section_one = Section.objects.get(slug='one')
        child_one = Section.objects.get(slug='introduction')

        count = report.modules_completed(self.participant)
        self.assertEquals(count, 0)

        UserPageVisit.objects.create(
            user=self.participant, section=section_one, status="complete")
        UserPageVisit.objects.create(
            user=self.participant, section=child_one, status="complete")
        count = report.modules_completed(self.participant)
        self.assertEquals(count, 1)

        section_two = Section.objects.get(slug='two')
        UserPageVisit.objects.create(
            user=self.participant, section=section_two,
            status="complete")
        count = report.modules_completed(self.participant)
        self.assertEquals(count, 2)

        section_four = Section.objects.get(slug='four')
        UserPageVisit.objects.create(
            user=self.participant, section=section_four,
            status="complete")
        count = report.modules_completed(self.participant)
        self.assertEquals(count, 3)

    def test_time_spent(self):
        report = ParticipantReport(self.hierarchy)

        module_one = Section.objects.get(slug='one')
        time_spent = report.time_spent(self.participant, module_one)
        self.assertEquals(time_spent, "00:00:00")

        now = datetime.datetime.now()
        section_one = Section.objects.get(slug='one')
        child_one = Section.objects.get(slug='introduction')

        visit = UserPageVisit.objects.create(
            user=self.participant, section=section_one, status="complete")
        delta = datetime.timedelta(minutes=-60)
        visit.first_visit = now + delta
        visit.save()

        visit = UserPageVisit.objects.create(
            user=self.participant, section=child_one, status="complete")
        delta = datetime.timedelta(minutes=-46)
        visit.first_visit = now + delta
        visit.save()

        time_spent = report.time_spent(self.participant, module_one)
        self.assertEquals(time_spent, "00:14:00")

        delta = datetime.timedelta(minutes=-25)
        visit.first_visit = now + delta
        visit.save()

        time_spent = report.time_spent(self.participant, module_one)
        self.assertEquals(time_spent, "00:05:00")

    def test_standalone_columns(self):
        report = ParticipantReport(self.hierarchy)
        columns = report.standalone_columns()
        self.assertEquals(len(columns), 15)

    def test_metadata(self):
        rows = [
            ['hierarchy', 'itemIdentifier', 'exercise type', 'itemType',
             'itemText', 'answerIdentifier', 'answerText'],
            '',
            ['', 'study_id', 'profile', 'string', 'Randomized Study Id'],
            ['', 'cohort_id', 'profile', 'string', 'Assigned Cohort Id'],
            ['', 'modules_completed', 'profile', 'count', 'modules completed'],
            ['', '1_time_spent', 'profile', 'string', 'One Time Spent'],
            ['', '1_encounter_id', 'profile', 'string', 'One Encounter Id'],
            ['', '1_first_makeup_id', 'profile', 'string',
             'One First Makeup Id'],
            ['', '1_second_makeup_id', 'profile', 'string',
             'One Second Makeup Id'],
            ['', '2_time_spent', 'profile', 'string', 'Two Time Spent'],
            ['', '2_encounter_id', 'profile', 'string', 'Two Encounter Id'],
            ['', '2_first_makeup_id', 'profile', 'string',
             'Two First Makeup Id'],
            ['', '2_second_makeup_id', 'profile', 'string',
             'Two Second Makeup Id'],
            ['', '3_time_spent', 'profile', 'string', 'Four Time Spent'],
            ['', '3_encounter_id', 'profile', 'string', 'Four Encounter Id'],
            ['', '3_first_makeup_id', 'profile', 'string',
             'Four First Makeup Id'],
            ['', '3_second_makeup_id', 'profile', 'string',
             'Four Second Makeup Id'],
            ['', 'supporter_count', 'Social Support Network', 'count',
             'Supporter Count'],
            ['', 'supporter_1_closeness', 'Social Support Network Map',
             'single choice', 'Supporter 1 Closeness', 'VC', 'Very Close'],
            ['', 'supporter_1_closeness', 'Social Support Network Map',
             'single choice', 'Supporter 1 Closeness', 'C', 'Close'],
            ['', 'supporter_1_closeness', 'Social Support Network Map',
             'single choice', 'Supporter 1 Closeness', 'NC', 'Not Close'],
            ['', 'supporter_1_influence', 'Social Support Network Map',
             'single choice', 'Supporter 1 Influence', 'P', 'Positive'],
            ['', 'supporter_1_influence', 'Social Support Network Map',
             'single choice', 'Supporter 1 Influence', 'MP',
             'Mostly Positive'],
            ['', 'supporter_1_influence', 'Social Support Network Map',
             'single choice', 'Supporter 1 Influence', 'MN',
             'Mostly Negative'],
            ['', 'supporter_1_influence', 'Social Support Network Map',
             'single choice', 'Supporter 1 Influence', 'N', 'Negative'],
            ['', 'supporter_1_provides_emotional_support',
             'Social Support Network Map', 'boolean',
             'Supporter 1 Provides_emotional_support', '', ''],
            ['', 'supporter_1_provides_practical_support',
             'Social Support Network Map', 'boolean',
             'Supporter 1 Provides_practical_support', '', '']
        ]

        report = ParticipantReport(self.hierarchy)
        metadata = report.metadata(Hierarchy.objects.all())
        for row in rows:
            self.assertEquals(metadata.next(), row)

        for x in range(0, 36):
            # expecting 9 more rows for additional 4 supporters
            # overkill to test every single value.
            metadata.next()

        with self.assertRaises(StopIteration):
            metadata.next()

    def test_values(self):
        rows = [
            ['study_id', 'cohort_id', 'modules_completed', '1_time_spent',
             '1_encounter_id', '1_first_makeup_id', '1_second_makeup_id',
             '2_time_spent', '2_encounter_id', '2_first_makeup_id',
             '2_second_makeup_id', '3_time_spent', '3_encounter_id',
             '3_first_makeup_id', '3_second_makeup_id', 'supporter_count',
             'supporter_1_closeness', 'supporter_1_influence',
             'supporter_1_provides_emotional_support',
             'supporter_1_provides_practical_support', 'supporter_2_closeness',
             'supporter_2_influence', 'supporter_2_provides_emotional_support',
             'supporter_2_provides_practical_support',
             'supporter_3_closeness', 'supporter_3_influence',
             'supporter_3_provides_emotional_support',
             'supporter_3_provides_practical_support', 'supporter_4_closeness',
             'supporter_4_influence', 'supporter_4_provides_emotional_support',
             'supporter_4_provides_practical_support', 'supporter_5_closeness',
             'supporter_5_influence', 'supporter_5_provides_emotional_support',
             'supporter_5_provides_practical_support']
        ]
        report = ParticipantReport(self.hierarchy)
        values = report.values(Hierarchy.objects.all())

        for row in rows:
            self.assertEquals(values.next(), row)

        with self.assertRaises(StopIteration):
            values.next()

    def test_post_not_logged_in(self):
        # not logged in
        response = self.client.post(self.report_url)
        self.assertEquals(response.status_code, 302)

    def test_post_keys(self):
        self.client.login(username=self.staff.username, password="test")
        data = {'report-type': 'keys'}
        response = self.client.post(self.report_url, data)
        self.assertEquals(response.status_code, 200)

    def test_post_values(self):
        self.client.login(username=self.staff.username, password="test")
        data = {'report-type': 'values'}
        response = self.client.post(self.report_url, data)
        self.assertEquals(response.status_code, 200)

    def test_post_facilitators(self):
        self.client.login(username=self.staff.username, password="test")
        data = {'report-type': 'facilitators'}
        response = self.client.post(self.report_url, data)
        self.assertEquals(response.status_code, 200)

        self.assertEquals(response.streaming_content.next(),
                          'Facilitator ID,Facilitator Name\r\n')

        val = 'f1,Facilitator One\r\n'
        self.assertTrue(val in response.streaming_content.next())

        with self.assertRaises(StopIteration):
            response.streaming_content.next()

    def test_post_locations(self):
        self.client.login(username=self.staff.username, password="test")
        data = {'report-type': 'locations'}
        response = self.client.post(self.report_url, data)
        self.assertEquals(response.status_code, 200)

        self.assertEquals(response.streaming_content.next(),
                          'Location ID,Location Name\r\n')
        val = 'Butler\r\n'
        self.assertTrue(val in response.streaming_content.next())

        with self.assertRaises(StopIteration):
            response.streaming_content.next()
