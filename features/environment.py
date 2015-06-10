from splinter import Browser
from behave_django import environment

from worth2.main.auth import generate_password
from worth2.main.tests.factories import (
    ParticipantFactory, WorthModuleFactory
)


BEHAVE_DEBUG_ON_ERROR = False


def before_all(context):
    context.browser = Browser('firefox')


def before_scenario(context, scenario):
    environment.before_scenario(context, scenario)
    # Set up mock worth data
    WorthModuleFactory()

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
    context.browser.quit()
    context.browser = None


def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        import ipdb
        ipdb.post_mortem(step.exc_traceback)
