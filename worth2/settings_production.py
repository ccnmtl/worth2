from worth2.settings_shared import *  # noqa: F403
from ctlsettings.production import common


locals().update(
    common(
        project=project,  # noqa: F405
        base=base,  # noqa: F405
        STATIC_ROOT=STATIC_ROOT,  # noqa: F405
        INSTALLED_APPS=INSTALLED_APPS,  # noqa: F405
        cloudfront="d1tpq2w6jljbie",
        s3prefix='ccnmtl',
    ))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

try:
    from worth2.local_settings import *  # noqa: F403 F401
except ImportError:
    pass
