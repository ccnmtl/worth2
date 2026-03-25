# flake8: noqa
from worth2.settings_shared import *
from ctlsettings.docker import common, init_sentry
import os

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
        s3prefix='ccnmtl',
    ))


SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    init_sentry(SENTRY_DSN)
