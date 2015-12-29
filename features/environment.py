from selenium import webdriver
from behave_django import environment
from django.conf import settings
from worth2.main.auth import generate_password
from worth2.main.tests.factories import (
    ParticipantFactory, UserFactory, WorthModuleFactory
)


def before_all(context):
    context.driver = webdriver.Firefox()
    # Wait up to 4 seconds for elements to appear.
    # http://selenium-python.readthedocs.org/en/latest/waits.html#implicit-waits
    context.driver.implicitly_wait(4)
    context.driver.set_page_load_timeout(30)


def before_scenario(context, scenario):
    environment.before_scenario(context, scenario)
    # Set up mock worth data
    WorthModuleFactory()

    facilitator = UserFactory()
    facilitator.set_password('facilitator_pass')
    facilitator.save()

    participant = ParticipantFactory()

    # This is taken from SignInParticipantTest. This is required
    # for the participant sign-in process to work correctly in
    # the tests.
    password = generate_password(participant.user.username)
    participant.user.set_password(password)
    participant.user.save()


def after_scenario(context, scenario):
    environment.after_scenario(context, scenario)


def after_all(context):
    context.driver.quit()


def after_step(context, step):
    if settings.BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        import ipdb
        ipdb.post_mortem(step.exc_traceback)
