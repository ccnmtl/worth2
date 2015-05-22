import urlparse
from splinter import Browser

from worth2.main.auth import generate_password
from worth2.main.tests.factories import (
    ParticipantFactory, WorthModuleFactory
)


BEHAVE_DEBUG_ON_ERROR = False


def before_all(context):
    host = context.host = 'localhost'
    port = context.port = 8081
    context.browser = Browser('firefox')

    # Set up mock worth data
    WorthModuleFactory()

    participant = ParticipantFactory()

    # This is taken from SignInParticipantTest. This is required
    # for the participant sign-in process to work correctly in
    # the tests.
    password = generate_password(participant.user.username)
    participant.user.set_password(password)
    participant.user.save()

    def browser_url(url):
        return urlparse.urljoin('http://%s:%d/' % (host, port), url)

    context.browser_url = browser_url


def after_all(context):
    context.browser.quit()
    context.browser = None


def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        import ipdb
        ipdb.post_mortem(step.exc_traceback)
