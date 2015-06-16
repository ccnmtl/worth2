# Django settings for worth2 project.
import os.path
import sys
from django.contrib import messages

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'worth2',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'worth2',
    }
}

# Media settings
MEDIA_URL = '/uploads/'
MEDIA_ROOT = 'uploads'
STATIC_URL = '/media/'
STATIC_ROOT = '/tmp/worth2/static/'
STATICFILES_DIRS = ('media/',)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
COMPRESS_URL = '/media/'
COMPRESS_ROOT = 'media/'
AWS_QUERYSTRING_AUTH = False

if 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }

if 'test' in sys.argv or 'jenkins' in sys.argv:
    MEDIA_ROOT = '/tmp/'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)
PROJECT_APPS = [
    'worth2.main',
]

ALLOWED_HOSTS = ['localhost', '.ccnmtl.columbia.edu']

USE_TZ = True
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False

SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'stagingcontext.staging_processor',
    'djangowind.context.context_processor',
    'django.template.context_processors.static',
    'django.template.context_processors.media',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'waffle.middleware.WaffleMiddleware',
)

ROOT_URLCONF = 'worth2.urls'

TEMPLATE_DIRS = (
    "/var/www/worth2/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_markwhat',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'sorl.thumbnail',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'ordered_model',
    'typogrify',
    'compressor',
    'django_statsd',
    'bootstrap3',
    'bootstrapform',
    'debug_toolbar',
    'waffle',
    'django_jenkins',
    'smoketest',
    'infranil',
    'flatblocks',
    'django_extensions',
    'impersonate',
    'registration',
    'pagetree',
    'pageblocks',
    'quizblock',
    'gunicorn',
    'rest_framework',
    'worth2.main',
    'worth2.protectivebehaviors',
    'worth2.ssnm',
    'worth2.goals',
    'worth2.selftalk',
    'behave_django',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'worth2.main.auth.IsActivePermission',
    )
}
REST_EMBER_FORMAT_KEYS = True
REST_EMBER_PLURALIZE_KEYS = True

PAGEBLOCKS = [
    'pageblocks.TextBlock',
    'pageblocks.HTMLBlock',
    'pageblocks.PullQuoteBlock',
    'main.SimpleImageBlock',
    'pageblocks.ImagePullQuoteBlock',
    'quizblock.Quiz',
    'main.AvatarSelectorBlock',
    'main.AvatarBlock',
    'main.VideoBlock',
    'protectivebehaviors.ProtectiveBehaviorsResults',
    'ssnm.SsnmPageBlock',
    'goals.GoalSettingBlock',
    'goals.GoalCheckInPageBlock',
    'selftalk.StatementBlock',
    'selftalk.RefutationBlock',
]


INTERNAL_IPS = ('127.0.0.1', )
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
)
DEBUG_TOOLBAR_PATCH_SETTINGS = False

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'worth2'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[worth2] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "worth2@ccnmtl.columbia.edu"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

# CAS settings
AUTHENTICATION_BACKENDS = ('djangowind.auth.SAMLAuthBackend',
                           'django.contrib.auth.backends.ModelBackend', )
CAS_BASE = "https://cas.columbia.edu/"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = ['djangowind.auth.AffilGroupMapper',
                       'djangowind.auth.StaffMapper',
                       'djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = [
    'anp8', 'jb2410', 'zm4', 'cld2156',
    'sld2131', 'amm8', 'mar227', 'jed2161', 'lrw2128', 'njn2118']

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
LOGIN_REDIRECT_URL = "/"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

ACCOUNT_ACTIVATION_DAYS = 7

# change on production / staging
PARTICIPANT_SECRET = 'something secret'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

BEHAVE_DEBUG_ON_ERROR = False
