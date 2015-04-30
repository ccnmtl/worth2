import urlparse
from splinter import Browser


BEHAVE_DEBUG_ON_ERROR = False


def before_all(context):
    host = context.host = 'localhost'
    port = context.port = 8081
    context.browser = Browser()

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
