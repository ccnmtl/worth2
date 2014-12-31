from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.db import models
from ordered_model.models import OrderedModel
from pagetree.models import Hierarchy, UserPageVisit


class InactiveUserProfile(models.Model):
    """ A model for handling inactive users.
    """
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


class Avatar(OrderedModel):
    """An image that the participant can choose for their profile."""

    class Meta(OrderedModel.Meta):
        pass

    image = models.ImageField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.image.url)


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
study_id_validator = RegexValidator(regex=r'^7.*$',
                                    message='That study ID isn\'t valid')


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

    # Participants can choose an avatar after their user is created.
    avatar = models.ForeignKey(Avatar, blank=True, null=True)


class Session(models.Model):
    facilitator = models.ForeignKey(User)
    participant = models.ForeignKey(Participant)
    location = models.ForeignKey(Location)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
