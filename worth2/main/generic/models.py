from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.db import models
from pagetree.models import Hierarchy, UserPageVisit, PageBlock


class BasePageBlock(models.Model):
    """An abstract pageblock to be used for custom pageblocks."""

    class Meta:
        abstract = True

    display_name = 'Unimplemented BasePageBlock'
    pageblocks = GenericRelation(PageBlock)

    def needs_submit(self):
        """Determines whether this pageblock needs form controls rendered.

        If needs_submit is True, then pagetree will create a <form>
        on this pageblock's surrounding page, and a Submit button for
        that form. It may also render a "Clear results" button, under
        the right circumstances. The surrounding <form> allows pagetree
        to handle form submissions for multiple blocks on the same page.

        Also, when needs_submit is True, the POST data on the Section's
        submit() step gets processed, but when needs_submit is False,
        nothing is sent to the server.

        :returns: a boolean
        """

        return False

    def unlocked(self, user):
        """Determines whether the user can proceed past this block.

        The current user is passed in to this function, allowing you to,
        for example, find out if that user has submitted the info
        necessary to proceed past this block's page.

        :param user: the current user
        :returns: a boolean
        """

        return True

    def submit(self, user, request_data):
        """Handle this pageblock's form submission.

        :returns: None
        """

        pass

    def redirect_to_self_on_submit(self):
        """Determines where the user is redirected to on page submission.

        If submit returns True, then the user will be redirected to the
        next page in the hierarchy. Otherwise, they be redirected to the
        current page.

        :returns: a boolean
        """

        return True

    def clear_user_submissions(self, user):
        """A hook to clear any user submissions for this block.

        :returns: None
        """

        pass

    def pageblock(self):
        return self.pageblocks.first()

    # TODO: I'd like to have all the following methods be inherited
    # somehow. For now these need to be copy and pasted for each custom
    # pageblock.
    @staticmethod
    def add_form():
        return BasePageBlockForm()

    def edit_form(self):
        return BasePageBlockForm(instance=self)

    @staticmethod
    def create(request):
        form = BasePageBlockForm(request.POST)
        return form.save()

    @classmethod
    def create_from_dict(cls, d):
        d.pop('block_type', None)
        d.pop('label', None)
        d.pop('css_extra', None)
        return cls.objects.create(**d)

    def edit(self, vals, files):
        form = BasePageBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class BasePageBlockForm(forms.ModelForm):
    """Example ModelForm for the BasePageBlock.

    This is just an example. It should always be replaced with your
    own ModelForm pointing to the custom pageblock.
    """

    class Meta:
        model = BasePageBlock


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
        hierarchy = Hierarchy.get_hierarchy('main')
        upv = UserPageVisit.objects.filter(
            user=self.user).order_by("-last_visit")
        if upv.count() < 1:
            return hierarchy.get_root()
        else:
            return upv.first().section

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

    def time_spent(self):
        """Returns the number of seconds the user has spent on the site."""
        visits = UserPageVisit.objects.filter(user=self.user)

        seconds = 0
        if (visits.count() > 0):
            start = visits.order_by('first_visit').first().first_visit
            end = visits.order_by('-last_visit').first().last_visit
            seconds = (end - start).total_seconds() / 60
        return seconds
