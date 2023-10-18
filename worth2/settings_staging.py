from django.conf import settings
from worth2.settings_shared import *  # noqa: F403
from ctlsettings.staging import common
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


locals().update(
    common(
        project=project,  # noqa: F405
        base=base,  # noqa: F405
        STATIC_ROOT=STATIC_ROOT,  # noqa: F405
        INSTALLED_APPS=INSTALLED_APPS,  # noqa: F405
        cloudfront="d1t432giinsu9y",
        s3prefix='ccnmtl',
    ))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

try:
    from worth2.local_settings import *  # noqa: F403
except ImportError:
    pass

if hasattr(settings, 'SENTRY_DSN'):
    sentry_sdk.init(
        dsn=SENTRY_DSN,  # noqa: F405
        integrations=[DjangoIntegration()],
        debug=True,
    )
