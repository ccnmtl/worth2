import base64
import hashlib
import hmac

from django.conf import settings
from django.contrib.auth.models import User


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
    return not user.is_anonymous() and \
        (hasattr(user, 'profile') and user.profile.is_participant())


def user_is_facilitator(user):
    return not user.is_anonymous() and \
        (not hasattr(user, 'profile') or not user.profile.is_participant())
