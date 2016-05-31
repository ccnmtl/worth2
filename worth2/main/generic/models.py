from __future__ import division

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from pagetree.models import Hierarchy, UserPageVisit


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
        """Returns the most recent location this user accessed.

        :rtype: UserPageVisit
        """
        return UserPageVisit.objects.filter(
            user=self.user).order_by('-last_visit').first()

    def last_access_in_module(self, module_num):
        """Returns the most recent location in the given module.

        :param: module_num int
        :rtype: UserPageVisit
        """
        main = Hierarchy.get_hierarchy('main')
        module_section = main.find_section_from_path(
            'session-{:d}'.format(module_num))
        if not module_section:
            return None

        pages = module_section.get_descendants()
        return UserPageVisit.objects.filter(
            user=self.user, section__in=pages
        ).order_by(
            '-last_visit').first()

    def last_location_url(self):
        if self.percent_complete_hierarchy() == 0:
            return reverse('root')
        else:
            return self.last_access_hierarchy().section.get_absolute_url()

    def percent_complete_by_pages(self, pages):
        page_count = float(pages.count())

        if page_count > 0:
            visits = UserPageVisit.objects.filter(
                user=self.user, section__in=pages).count()
            return int(visits / page_count * 100)
        else:
            return 0

    def percent_complete_hierarchy(self):
        hierarchy = Hierarchy.get_hierarchy('main')
        pages = hierarchy.get_root().get_descendants()
        return self.percent_complete_by_pages(pages)

    def percent_complete_module(self, module_num):
        """
        Return the percentage of the given module that has been completed
        by this participant. Sections are considered "completed" if they
        have been accessed, (i.e., if there is a UserPageVisit)

        :rtype: int
        """
        main = Hierarchy.get_hierarchy('main')
        module_section = main.find_section_from_path(
            'session-{:d}'.format(module_num))
        if not module_section:
            return 0

        pages = module_section.get_descendants()
        return self.percent_complete_by_pages(pages)
