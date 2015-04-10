from datetime import timedelta

from django.contrib.auth.models import User
from django.core.cache import cache
from pagetree.models import UserPageVisit
from pagetree.reports import PagetreeReport, StandaloneReportColumn


class ParticipantReport(PagetreeReport):

    five_minutes = timedelta(minutes=5)
    fifteen_minutes = timedelta(minutes=15)

    @classmethod
    def get_descendants(cls, section):
        key = 'hierarchy_%s_section_%s' % (section.hierarchy.id, section.id)
        descendants = cache.get(key)
        if descendants is None:
            descendants = section.get_descendants()
            cache.set(key, descendants)
        return descendants

    @classmethod
    def get_descendant_ids(cls, section):
        key = 'hierarchy_%s_sectionids_%s' % (section.hierarchy.id, section.id)
        ids = cache.get(key)
        if ids is None:
            descendants = cls.get_descendants(section)
            ids = [s.id for s in descendants]
            cache.set(key, ids)
        return ids

    @classmethod
    def format_timedelta(cls, delta):
        hours, remainder = divmod(delta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return '%02d:%02d:%02d' % (hours, minutes, seconds)

    def __init__(self, hierarchy):
        self.hierarchy = hierarchy
        super(ParticipantReport, self).__init__()

    def users(self):
        users = User.objects.filter(is_active=False,
                                    userpagevisit__isnull=False).distinct()
        return users.order_by('id')

    def percent_complete(self, user, section):
        section_ids = self.get_descendant_ids(section)
        if not section.is_root():
            section_ids.insert(0, section.id)

        count = len(section_ids)
        if count == 0:
            return 0
        else:
            visits = UserPageVisit.objects.filter(user=user,
                                                  status='complete',
                                                  section__in=section_ids)
            return len(visits) / float(count) * 100

    def modules_completed(self, user):
        complete = 0

        for module in self.hierarchy.get_root().get_children():
            if self.percent_complete(user, module) == 100:
                complete += 1
            else:
                break
        return complete

    def time_spent(self, user, section):
        section_ids = self.get_descendant_ids(section)
        section_ids.insert(0, section.id)

        visits = UserPageVisit.objects.filter(user=user,
                                              status='complete',
                                              section__in=section_ids)

        time_spent = timedelta(0)
        prev = None
        for page in visits.order_by('first_visit'):
            if prev:
                interval = (page.first_visit - prev)
                if interval > self.fifteen_minutes:
                    # record 5 minutes for any interval longer than 15 minutes
                    time_spent += min(interval, self.five_minutes)
                else:
                    time_spent += interval
            prev = page.first_visit

        return self.format_timedelta(time_spent)

    def per_module_columns(self, idx, module):
        return [
            StandaloneReportColumn(
                '%s_time_spent' % idx, 'profile', 'string',
                'Time Spent in %s' % module.label,
                lambda x: self.time_spent(x, module)),
            StandaloneReportColumn(
                '%s_encounter' % idx, 'profile', 'string',
                '%s Encounter' % module.label,
                lambda x: x.profile.participant.encounter_id(module, idx, 0)),
            StandaloneReportColumn(
                '%s_first_makeup' % idx, 'profile', 'string',
                '%s First Makeup' % module.label,
                lambda x: x.profile.participant.encounter_id(module, idx, 1)),
            StandaloneReportColumn(
                '%s_second_makeup' % idx, 'profile', 'string',
                '%s Second Makeup' % module.label,
                lambda x: x.profile.participant.encounter_id(module, idx, 2))
        ]

    def standalone_columns(self):
        base_columns = [
            StandaloneReportColumn(
                'study_id', 'profile', 'string', 'Randomized Study Id',
                lambda x: x.profile.participant.study_id),
            StandaloneReportColumn(
                'cohort_id', 'profile', 'string', 'Assigned Cohort Id',
                lambda x: x.profile.participant.cohort_id),
            StandaloneReportColumn(
                'modules_completed', 'profile', 'count', 'modules completed',
                lambda x: self.modules_completed(x)),
        ]

        for idx, module in enumerate(self.hierarchy.get_root().get_children()):
            base_columns += self.per_module_columns(idx, module)

        return base_columns
