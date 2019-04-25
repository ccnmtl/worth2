# flake8: noqa
from worth2.settings_shared import *

try:
    from worth2.local_settings import *
except ImportError:
    pass
