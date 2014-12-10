from django.core.validators import RegexValidator
from django.db import models
from ordered_model.models import OrderedModel

from worth2.main.mixins import InactiveProfileMixin


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


class Participant(InactiveProfileMixin, models.Model):
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
