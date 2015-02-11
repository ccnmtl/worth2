from rest_framework import authentication
from rest_framework import permissions


class InactiveUserSessionAuthentication(authentication.BaseAuthentication):
    """ Authenticate an inactive user, i.e. a Participant """
    def authenticate(self, request):
        # Get user from underlying HttpRequest, just like
        # rest_framework.authentication.SessionAuthentication
        request = request._request
        user = getattr(request, 'user', None)
        return (user, None)


class IsParticipantPermission(permissions.BasePermission):
    """ Give participants permission. """
    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        return user and hasattr(user, 'profile') and \
            user.profile.is_participant()
