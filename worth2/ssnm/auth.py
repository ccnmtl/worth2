from rest_framework import authentication


class InactiveUserSessionAuthentication(authentication.BaseAuthentication):
    """ Authenticate an inactive user, i.e. a Participant """
    def authenticate(self, request):
        # Get user from underlying HttpRequest, just like
        # rest_framework.authentication.SessionAuthentication
        request = request._request
        user = getattr(request, 'user', None)
        return (user, None)
