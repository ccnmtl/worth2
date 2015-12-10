# Django settings for worth2 project.
import os.path
import sys
from django.contrib import messages

from ccnmtlsettings.shared import common

project = 'worth2'
base = os.path.dirname(__file__)
locals().update(common(project=project, base=base))

if 'test' in sys.argv or 'jenkins' in sys.argv:
    MEDIA_ROOT = '/tmp/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'worth2',
    }
}

PROJECT_APPS = [
    'worth2.main',
]

USE_TZ = True

MIDDLEWARE_CLASSES += [  # noqa
    'django.middleware.csrf.CsrfViewMiddleware',
]

INSTALLED_APPS += [  # noqa
    'sorl.thumbnail',
    'django.contrib.webdesign',
    'ordered_model',
    'typogrify',
    'bootstrap3',
    'bootstrapform',
    'infranil',
    'django_extensions',
    'registration',
    'pagetree',
    'pageblocks',
    'quizblock',
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

LOGIN_REDIRECT_URL = "/"

ACCOUNT_ACTIVATION_DAYS = 7

# change on production / staging
PARTICIPANT_SECRET = 'something secret'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

BEHAVE_DEBUG_ON_ERROR = False
