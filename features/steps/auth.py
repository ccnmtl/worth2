import urlparse
from behave import given, when
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.auth.models import User
from django.utils.module_loading import import_module
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from worth2.main.auth import generate_password
from worth2.main.models import Location, Participant


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
    d = context.driver

    # We need to visit a page on this domain in order
    # to create a cookie for it.

    d.get('/some_404_page/')

    d.find_element_by_xpath('//body')
    user, s = create_pre_authenticated_session(user_type)
    d.add_cookie({'name': settings.SESSION_COOKIE_NAME, 'value': s})
    context.user = user


@when(u'I sign in as a facilitator')
def i_sign_in_as_a_facilitator(context):
    facilitator = User.objects.filter(is_active=True).first()

    d = context.driver
    d.get(urlparse.urljoin(context.base_url, '/accounts/login/'))
    username = d.find_element_by_name('username')
    password = d.find_element_by_name('password')
    username.send_keys(facilitator.username)
    password.send_keys('facilitator_pass')

    d.find_element_by_class_name('form-signin').submit()


@when(u'I sign in as a participant')
def i_sign_in_as_a_participant(context):
    i_sign_in_as_a_facilitator(context)

    participant = Participant.objects.first()
    password = generate_password(participant.user.username)
    participant.user.set_password(password)
    participant.user.save()

    location = Location.objects.first()

    d = context.driver
    d.get(urlparse.urljoin(context.base_url, '/sign-in-participant/'))
    Select(d.find_element_by_name(
        'participant_id')).select_by_value(unicode(participant.pk))
    Select(d.find_element_by_name(
        'participant_location')).select_by_value(unicode(location.pk))
    d.find_elements_by_css_selector(
        'input[type="radio"][name="participant_destination"]')[0].click()
    d.find_elements_by_css_selector(
        'input[type="radio"][name="session_type"]')[0].click()
    d.find_element_by_css_selector(
        '.worth-facilitator-sign-in-participant button[type="submit"]'
    ).click()


@when(u'I sign in as the facilitator from a session')
def i_sign_in_as_the_facilitator_from_a_session(context):
    d = context.driver
    facilitator = User.objects.filter(is_active=True).first()

    try:
        # If the window is narrow, we need to click the collapse
        # button first.
        element = d.find_element_by_id('worth-collapse-button')
        element.click()
    except ElementNotVisibleException:
        pass

    wait = WebDriverWait(d, 10)
    element = wait.until(
        expected_conditions.element_to_be_clickable(
            (By.ID, 'worth-facilitator-button')))
    element.click()

    wait = WebDriverWait(d, 10)
    element = wait.until(
        expected_conditions.visibility_of_element_located(
            (By.NAME, 'facilitator_username')))
    element.send_keys(facilitator.username)

    wait = WebDriverWait(d, 10)
    element = wait.until(
        expected_conditions.visibility_of_element_located(
            (By.NAME, 'facilitator_password')))
    element.send_keys('facilitator_pass')

    wait = WebDriverWait(d, 10)
    element = wait.until(
        expected_conditions.element_to_be_clickable(
            (By.ID, 'worth-sign-out-participant-submit')))
    element.click()
