# Django settings for authserver project.
import sys

###############################################################################
# DEBUG
###############################################################################

DEBUG = True
TEMPLATE_DEBUG = DEBUG

###############################################################################
# Auth
###############################################################################

AUTH_USER_MODEL = 'authserver.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'PAGINATE_BY': 20,

    'DEFAULT_AUTHENTICATION_CLASSES': (),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'authserver.parsers.BetterJSONParser',
        'authserver.parsers.BetterFormParser'
    ),

    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

AUTHENTICATION_BACKENDS = ()

###############################################################################
# CORS AND COOKIES
###############################################################################

SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None

APPEND_SLASH = False

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

###############################################################################
# TESTING
###############################################################################

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# NOSE_ARGS = [
#     '--logging-clear-handlers',
#     '--verbosity=2',
#     '--with-yanc',
# ]


###############################################################################
# DATABASES
###############################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'authserver',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

###############################################################################
# APP
###############################################################################

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = False

SECRET_KEY = 'sipd&_7_kw2cg-985=*v#)^&hx_h)t)k7io$ag5p__f5vfdjm!'
ROOT_URLCONF = 'authserver_project.urls'
WSGI_APPLICATION = 'authserver_project.wsgi.application'

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
)

INSTALLED_APPS = [
    'authserver',
    'rest_framework',
    'django_extensions',
]

###############################################################################
# LOGGING
###############################################################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(thread)d [%(levelname)s] [%(pathname)s %(funcName)s] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'analytics': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propogate': True,
        },
    },
}
