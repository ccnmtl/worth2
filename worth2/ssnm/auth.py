from rest_framework.authentication import SessionAuthentication


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
