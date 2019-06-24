# Django settings for worth2 project.
import os.path
import sys
from django.contrib import messages

from ccnmtlsettings.shared import common

project = 'worth2'
base = os.path.dirname(__file__)
locals().update(common(project=project, base=base))

if 'test' in sys.argv or 'jenkins' in sys.argv or 'behave' in sys.argv:
    MEDIA_ROOT = '/tmp/'  # nosec

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'worth2',
    }
}

PROJECT_APPS = [
    'worth2.main',
    'worth2.goals',
    'worth2.protectivebehaviors',
    'worth2.selftalk',
    'worth2.ssnm',
]

USE_TZ = True

MIDDLEWARE += [  # noqa
    'django.middleware.csrf.CsrfViewMiddleware',
]

INSTALLED_APPS += [  # noqa
    'sorl.thumbnail',
    'ordered_model',
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
    'pagetreeepub',
]

JSON_API_PLURALIZE_TYPES = True

PAGEBLOCKS = [
    'pageblocks.TextBlock',
    'pageblocks.HTMLBlock',
    'main.SimpleImageBlock',
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

# epub settings
EPUB_ALLOWED_BLOCKS = [
    'Text Block', 'HTML Block', 'Pull Quote'
]
EPUB_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates/epub")
EPUB_TITLE = "WORTH epub"
EPUB_CREATOR = "CTL"
EPUB_PUBLICATION = "2017"
