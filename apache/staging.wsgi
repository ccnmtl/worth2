import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/worth2/worth2/ve/lib/python2.7/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/worth2/worth2/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'worth2.settings_staging'

import django.core.handlers.wsgi
import django
django.setup()

application = django.core.handlers.wsgi.WSGIHandler()
