import os
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "worth2.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
