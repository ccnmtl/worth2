from django import template

register = template.Library()


@register.simple_tag
def avatar_url(user):
    """Returns the url for the current user's avatar.

    Admins are given a default avatar, and participants are given their
    chosen avatar.
    """
    url = ''
    if user.is_staff or user.is_superuser:
        # Provide a default url for admins, for testing purposes
        t = template.Template('{% load static %}{% static url %}')
        url = t.render(template.Context({'url': 'admin-avatar.png'}))
    elif hasattr(user, 'profile') and user.profile.is_participant():
        if user.profile.participant.avatar:
            # This will be the complete s3 url
            url = user.profile.participant.avatar.image.url
    return url
