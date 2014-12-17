from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from pagetree.models import Hierarchy, UserPageVisit


class InactiveProfileMixin(models.Model):
    """A mixin for creating inactive users.
    """

    # Set an explicit primary key, to not clash with those of any models
    # that use this mixin.
    user_profile_id = models.AutoField(primary_key=True)

    user = models.OneToOneField(User, related_name='profile')
    created_by = models.ForeignKey(User, null=True, blank=True,
                                   related_name='created_by')
    is_archived = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def is_participant(self):
        return (not self.user.is_active)

    def default_location(self):
        hierarchy = Hierarchy.get_hierarchy()
        return hierarchy.get_root()

    def last_access(self):
        return self.last_access_hierarchy() or self.created

    def last_access_formatted(self):
        dt = self.last_access_hierarchy()
        return dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else ''

    def last_access_hierarchy(self):
        upv = UserPageVisit.objects.filter(
            user=self.user).order_by(
                "-last_visit")
        if upv.count() < 1:
            return None
        else:
            return upv[0].last_visit

    def last_location_url(self):
        if self.percent_complete() == 0:
            return reverse('root')
        else:
            return self.last_location().get_absolute_url()

    def last_location(self):
        hierarchy = Hierarchy.get_hierarchy()
        upv = UserPageVisit.objects.filter(
            user=self.user).order_by(
                "-last_visit")
        if upv.count() < 1:
            return hierarchy.get_root()
        else:
            return upv[0].section

    def percent_complete(self):
        return self.percent_complete_hierarchy()

    def percent_complete_hierarchy(self):
        hierarchy = Hierarchy.get_hierarchy()
        pages = len(hierarchy.get_root().get_descendants())
        visits = UserPageVisit.objects.filter(user=self.user).count()

        if pages:
            return int(visits / float(pages) * 100)
        else:
            return 0

    def time_spent(self):
        visits = UserPageVisit.objects.filter(user=self.user)

        seconds = 0
        if (visits.count() > 0):
            start = visits.order_by('first_visit')[0].first_visit
            end = visits.order_by('-last_visit')[0].last_visit
            seconds = (end - start).total_seconds() / 60
        return seconds
