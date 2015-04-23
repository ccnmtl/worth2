from django import template

from worth2.main.models import Participant

register = template.Library()


@register.assignment_tag
def get_participant(pk):
    """Returns a participant, given their primary key."""
    return Participant.objects.get(pk=pk)
