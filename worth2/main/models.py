from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.db import models
from django.shortcuts import get_object_or_404
from ordered_model.models import OrderedModel
from pagetree.models import Hierarchy, UserPageVisit, PageBlock

from worth2.main.auth import user_is_participant


class InactiveUserProfile(models.Model):
    """A model for handling inactive users."""

    user = models.OneToOneField(User, related_name='profile')
    created_by = models.ForeignKey(User, null=True, blank=True,
                                   related_name='created_by')
    is_archived = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return unicode(self.user.username)

    def is_participant(self):
        return (not self.user.is_active)

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
        visits = UserPageVisit.objects.filter(user=self.user)

        seconds = 0
        if (visits.count() > 0):
            start = visits.order_by('first_visit').first().first_visit
            end = visits.order_by('-last_visit').first().last_visit
            seconds = (end - start).total_seconds() / 60
        return seconds


class Avatar(OrderedModel):
    """An image that the participant can choose for their profile."""

    class Meta(OrderedModel.Meta):
        pass

    image = models.ImageField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.image.url)


class AvatarBlock(models.Model):
    """A PageBlock for displaying the current participant's avatar."""

    display_name = 'Avatar Block'
    pageblocks = GenericRelation(PageBlock)
    template_file = 'main/avatar_block.html'

    def pageblock(self):
        return self.pageblocks.first()

    def needs_submit(self):
        return True

    @classmethod
    def add_form(cls):
        return AvatarBlockForm()

    def edit_form(self):
        return AvatarBlockForm(instance=self)

    @classmethod
    def create(cls, request):
        form = AvatarBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = AvatarBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True


class AvatarBlockForm(forms.ModelForm):
    class Meta:
        model = AvatarBlock


class AvatarSelectorBlock(models.Model):
    """A PageBlock for displaying the Avatar Selector."""

    display_name = 'Avatar Selector Block'
    pageblocks = GenericRelation(PageBlock)
    template_file = 'main/avatar_selector_block.html'

    def pageblock(self):
        return self.pageblocks.first()

    def needs_submit(self):
        return True

    @classmethod
    def add_form(cls):
        return AvatarSelectorBlockForm()

    def edit_form(self):
        return AvatarSelectorBlockForm(instance=self)

    @classmethod
    def create(cls, request):
        form = AvatarSelectorBlockForm(request.POST)
        return form.save()

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create()

    def edit(self, vals, files):
        form = AvatarSelectorBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True

    def avatars(self):
        """Returns a queryset of all the available avatars in WORTH."""

        return Avatar.objects.all()

    def submit(self, user, request_data):
        if user_is_participant(user):
            avatar_id = request_data.get('avatar-id')
            avatar = get_object_or_404(Avatar, pk=avatar_id)
            user.profile.participant.avatar = avatar
            user.profile.participant.save()


class AvatarSelectorBlockForm(forms.ModelForm):
    class Meta:
        model = AvatarSelectorBlock


class Location(models.Model):
    """A physical location where an intervention takes place.

    Time and place are used to create the participants' cohort
    (implemented as a group).
    """

    name = models.TextField()

    def __unicode__(self):
        return unicode(self.name)


# A user in WORTH 2 can either be:
# - A participant
# - A facilitator
# - A research assistant
# - A researcher
# - A superuser
#
# Some of these types of users have special data associated with them.

# We don't know what this format will be yet, so for now just test
# validation by only accepting strings that begin with a '7'
study_id_validator = RegexValidator(
    regex=r'^7.*$',
    message='That study ID isn\'t valid. (It needs to start with a 7)')

# For now, accept any 3-digit number as the cohort ID.
cohort_id_validator = RegexValidator(
    regex=r'^\d{3}$',
    message='That cohort ID isn\'t valid. (It needs to be 3 digits)')


class ParticipantManager(models.Manager):
    def cohort_ids(self):
        """
        Get a list of all the unique cohort IDs that have been entered
        on the participants.
        """

        ids = self.all().values_list(
            'cohort_id', flat=True
        ).exclude(
            cohort_id__isnull=True
        ).exclude(
            cohort_id__exact='').distinct()

        return sorted(ids)


class Participant(InactiveUserProfile):
    """ A Participant is a worth-specific inactive user profile.
    """
    # first_location is set the first time that a facilitator signs in a
    # participant. This is used to infer the participant's cohort group.
    first_location = models.ForeignKey(Location, blank=True, null=True,
                                       related_name='first_location')

    # location is set each time a facilitator signs in a participant.
    location = models.ForeignKey(Location, blank=True, null=True)

    # A study ID is pre-generated for each participant, and then entered
    # into our system.
    study_id = models.CharField(max_length=255,
                                unique=True,
                                db_index=True,
                                validators=[study_id_validator])

    # The cohort ID is assigned when the participant begins the second
    # session. It represents the group of all the participants present
    # for that session. It doesn't change for subsequent sessions, even
    # though there may be different participants present.
    cohort_id = models.CharField(max_length=255,
                                 blank=True,
                                 null=True,
                                 db_index=True,
                                 validators=[cohort_id_validator])

    # Participants can choose an avatar after their user is created.
    avatar = models.ForeignKey(Avatar, blank=True, null=True)

    objects = ParticipantManager()

    def __unicode__(self):
        return unicode(self.study_id)


class Session(models.Model):
    """A Session represents a participant going through a WORTH session.

    A Session is created each time a facilitator logs in a participant.
    """

    facilitator = models.ForeignKey(User)
    participant = models.ForeignKey(Participant)
    location = models.ForeignKey(Location)
    session_type = models.CharField(
        max_length=255,
        choices=(('regular', 'Regular'), ('makeup', 'Make-Up')),
        default='regular',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode('Session for ' + self.participant.user.username)


class VideoBlock(models.Model):
    display_name = 'Video Block'
    pageblocks = GenericRelation(PageBlock)
    template_file = 'main/video_block.html'
    js_template_file = 'main/video_block_js.html'
    css_template_file = 'main/video_block_css.html'

    video_url = models.URLField(max_length=255)

    def pageblock(self):
        return self.pageblocks.first()

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return VideoBlockForm()

    def edit_form(self):
        return VideoBlockForm(instance=self)

    @classmethod
    def create(self, request):
        form = VideoBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = VideoBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True


class VideoBlockForm(forms.ModelForm):
    class Meta:
        model = VideoBlock
