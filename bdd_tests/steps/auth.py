from behave import given
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.utils.module_loading import import_module
from splinter.request_handler.status_code import HttpResponseError

from worth2.main.tests.factories import UserFactory, ParticipantFactory


def create_pre_authenticated_session(user_type):
    if user_type == 'participant':
        user = ParticipantFactory()
    else:
        user = UserFactory()
    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return user, session.session_key


@given(u'I am signed in as a {user_type}')
def i_am_signed_in_as_a(context, user_type):
    if hasattr(context, 'user') and context.user is not None:
        # already logged in
        return
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
