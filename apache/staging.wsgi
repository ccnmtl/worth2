import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/worth2/worth2/ve/lib/python2.7/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/worth2/worth2/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'worth2.settings_staging'

import django
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
