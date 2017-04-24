import base64
import hashlib
import hmac

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication


def generate_random_username():
    random_number = User.objects.make_random_password(
        length=7, allowed_chars='123456789')

    while User.objects.filter(username=random_number):
        random_number = User.objects.make_random_password(
            length=7, allowed_chars='123456789')

    return "%s%s" % ('participant_', random_number)


def generate_password(username):
    digest = hmac.new(settings.PARTICIPANT_SECRET,
                      msg=username, digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def user_is_participant(user):
    return not user.is_anonymous and \
        (hasattr(user, 'profile') and user.profile.is_participant())


def user_is_facilitator(user):
    """
    Any normal user that can log in (has is_active=True) is considered
    a facilitator in WORTH. Participants are 'authenticated' users, but
    are not 'active'. So this permission is granted to anyone in the
    system except for the participants.
    """

    return (hasattr(user, 'is_active') and user.is_active)


class IsActivePermission(permissions.BasePermission):
    """A DRF permission to give facilitators and admins access."""

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        return user_is_facilitator(user)


class IsParticipantPermission(permissions.BasePermission):
    """A DRF permission to give participants permission."""
    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        return user_is_participant(user)


class AnySessionAuthentication(SessionAuthentication):
    """Authenticate any user, whether active or inactive.

    This is very similar to django-rest-framework's
    SessionAuthentication. The only difference is that this will
    authenticate users who are inactive as well as active.

    Participants are inactive in worth, so this lets them use SSNM's API.
    """

    def authenticate(self, request):
        # Get user from underlying HttpRequest, just like
        # rest_framework.authentication.SessionAuthentication
        request = request._request
        user = getattr(request, 'user', None)

        self.enforce_csrf(request)

        return (user, None)
