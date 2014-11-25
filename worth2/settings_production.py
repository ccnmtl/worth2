# flake8: noqa
from settings_shared import *
import os
import sys

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

MEDIA_ROOT = '/var/www/worth2/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/worth2/worth2/sitemedia'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'worth2',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
    }
}

COMPRESS_ROOT = "/var/www/worth2/worth2/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')				

try:
    from local_settings import *
except ImportError:
    pass
