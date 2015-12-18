import urlparse
from behave import given, when
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.auth.models import User
from django.utils.module_loading import import_module
from splinter.request_handler.status_code import HttpResponseError
from worth2.main.auth import generate_password
from worth2.main.models import Location, Participant
from worth2.main.tests.factories import UserFactory


def create_pre_authenticated_session(user_type):
    if user_type == 'participant':
        # TODO: why doesn't this work on participants?
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
        b.driver.get('/some_404_page/')
    except HttpResponseError:
        pass

    b.find_by_xpath('//body')
    user, s = create_pre_authenticated_session(user_type)
    b.cookies.add({'name': settings.SESSION_COOKIE_NAME, 'value': s})
    context.user = user


@when(u'I sign in as a facilitator')
def i_sign_in_as_a_facilitator(context):
    facilitator = UserFactory()
    facilitator.set_password('test_pass')
    facilitator.save()

    b = context.browser
    b.driver.get(urlparse.urljoin(context.base_url, '/accounts/login/'))
    b.fill('username', facilitator.username)
    b.fill('password', 'test_pass')

    old_url = context.browser.url
    link = b.driver.find_element_by_css_selector(
        '.form-signin button[type="submit"]')

    link.click()
    # If the url didn't change, it might need another click
    if old_url == context.browser.url:
        link.click()


@when(u'I sign in as a participant')
def i_sign_in_as_a_participant(context):
    i_sign_in_as_a_facilitator(context)

    participant = Participant.objects.first()
    password = generate_password(participant.user.username)
    participant.user.set_password(password)
    participant.user.save()

    location = Location.objects.first()

    b = context.browser
    b.driver.get(urlparse.urljoin(context.base_url, '/sign-in-participant/'))
    b.select('participant_id', participant.pk)
    b.select('participant_location', location.pk)
    b.choose('participant_destination', '1')
    b.choose('session_type', 'regular')
    b.find_by_css(
        '.worth-facilitator-sign-in-participant button[type="submit"]'
    ).first.click()


@when(u'I sign in as the facilitator from a session')
def i_sign_in_as_the_facilitator_from_a_session(context):
    b = context.browser
    b.find_by_text('Facilitator').first.click()
    facilitator = User.objects.filter(is_active=True).first()
    b.fill('facilitator_username', facilitator.username)
    b.fill('facilitator_password', 'test')
    b.find_by_css(
        '.worth-sign-out-participant button[type="submit"]').first.click()
