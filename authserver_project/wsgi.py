import os

# Monkey patch urllib etc
from gevent import monkey
monkey.patch_socket()

# Monkey patch db
from psycogreen.gevent import patch_psycopg
patch_psycopg()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "authserver_project.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
