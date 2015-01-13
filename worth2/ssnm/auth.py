from rest_framework import authentication


class InactiveUserSessionAuthentication(authentication.BaseAuthentication):
    """ Authenticate an inactive user, i.e. a Participant """
    def authenticate(self, request):
        # TODO
        user = getattr(request, 'user', None)
        return (user, None)
