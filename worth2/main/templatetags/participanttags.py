from datetime import timedelta
from django import template
from django.utils import timezone

from worth2.main.utils import percent_complete_by_module

register = template.Library()


@register.filter
def is_recent(dt):
    """Returns True if the given datetime is within 5 mins of now."""
    if dt is None:
        return False

    return (timezone.now() - dt) < timedelta(minutes=5)


@register.simple_tag
def module_completed_percentage(user, module):
    return percent_complete_by_module(user, module)
