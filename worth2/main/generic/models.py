from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from pagetree.models import Hierarchy, UserPageVisit
from worth2.main.utils import get_verbose_section_name


class BaseUserProfile(models.Model):
    """An abstract class for a user profile."""

    class Meta:
        abstract = True

    user = models.OneToOneField(User, related_name='profile')
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return unicode(self.user.username)

    def default_location(self):
        hierarchy = Hierarchy.get_hierarchy('main')
        return hierarchy.get_root()

    def last_access(self):
        return self.last_access_hierarchy() or self.created

    def last_access_formatted(self):
        dt = self.last_access_hierarchy()
        return dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else ''

    def last_access_hierarchy(self):
        upv = UserPageVisit.objects.filter(
            user=self.user).order_by("-last_visit")
        if upv.count() < 1:
            return None
        else:
            return upv.first().last_visit

    def last_location_url(self):
        if self.percent_complete() == 0:
            return reverse('root')
        else:
            return self.last_location().get_absolute_url()

    def last_location(self):
        """Returns the last location this user accessed.

        If the user hasn't accessed any sections, this function returns
        None.

        :rtype: Section
        """
        visits = UserPageVisit.objects.filter(
            user=self.user).order_by("-last_visit")
        if visits.count() > 0:
            return visits.first().section
        else:
            return None

    def last_location_verbose(self):
        return get_verbose_section_name(self.last_location())

    def next_location_verbose(self):
        last_location = self.last_location()
        if last_location:
            return get_verbose_section_name(last_location.get_next())
        else:
            return None

    def percent_complete(self):
        return self.percent_complete_hierarchy()

    def percent_complete_hierarchy(self):
        hierarchy = Hierarchy.get_hierarchy('main')
        pages = len(hierarchy.get_root().get_descendants())
        visits = UserPageVisit.objects.filter(user=self.user).count()

        if pages:
            return int(visits / float(pages) * 100)
        else:
            return 0
