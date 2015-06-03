from behave import given
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.auth.models import User
from django.utils.module_loading import import_module
from splinter.request_handler.status_code import HttpResponseError

from worth2.main.models import Participant


def create_pre_authenticated_session(user_type):
    if user_type == 'participant':
        # TODO: why this work on participants?
        participant = Participant.objects.first()
        user = participant.user
    else:
        user = User.objects.first()
    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return user, session.session_key


@given(u'I am signed in as a {user_type}')
def i_am_signed_in_as_a(context, user_type):
    if hasattr(context, 'user') and context.user is not None:
        # Already logged in, so clear the existing session.
        context.request.session.flush()
    b = context.browser

    # We need to visit a page on this domain in order
    # to create a cookie for it.
    try:
        # 404 pages raise an exception in splinter
        b.visit(context.browser_url('/some_404_page/'))
    except HttpResponseError:
        pass

    b.find_by_xpath('//body')
    user, s = create_pre_authenticated_session(user_type)
    b.cookies.add({'name': settings.SESSION_COOKIE_NAME, 'value': s})
    context.user = user


@given(u'I am not logged in')
def i_am_not_logged_in(context):
    context.browser.cookies.delete()
    try:
        context.user = None
    except:
        pass
