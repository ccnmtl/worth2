from django.db import models
from ordered_model.models import OrderedModel

from worth2.main.mixins import UserProfileMixin


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


class Participant(UserProfileMixin, models.Model):
    location = models.ForeignKey(Location)

    # A study ID is generated for each participant.
    study_id = models.PositiveIntegerField()

    # Participants can choose an avatar after their user is created.
    avatar = models.ForeignKey(Avatar, null=True)
