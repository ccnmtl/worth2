from datetime import timedelta
from django import template
from django.utils import timezone

from worth2.main.models import Participant

register = template.Library()


@register.simple_tag
def get_participant(pk):
    """Returns a participant, given their primary key."""
    return Participant.objects.get(pk=pk)


@register.filter
def is_recent(dt):
    """Returns True if the given datetime is within 5 mins of now."""
    if dt is None:
        return False

    return (timezone.now() - dt) < timedelta(minutes=5)
