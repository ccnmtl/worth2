from django import template

from worth2.main.models import Avatar

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
    elif hasattr(user, 'profile2'):
        if user.profile2.avatar:
            # This will be the complete s3 url
            url = user.profile2.avatar.image.url
        else:
            default_avatar = Avatar.objects.filter(is_default=True).first()
            if default_avatar:
                url = default_avatar.image.url

    return url
