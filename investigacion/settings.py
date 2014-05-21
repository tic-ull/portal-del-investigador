# -*- encoding: UTF-8 -*-

"""
Django settings for investigacion project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z7(##tnkvh@@h@rcpcu+&v=nyy!(nt1y6a8ovb5l7yk04bxh3+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

DEVEL = True

ADMINS = (
    ('STIC-Investigacion', 'stic.investigacion@ull.es'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django.contrib.sites',  # Flatpages
    'django.contrib.flatpages',
    'tinymce',  # Flatpages tinymce
    #'flatpages_tinymce',
    'south',
    'core',
    'cvn',
    'bootstrap_toolkit',
    'crequest',
    'django_coverage',
)

COVERAGE_MODULE_EXCLUDES = (
    'tests$', 'settings$', 'urls$', 'locale$', 'common.views.test', '__init__',
    'django', 'migrations', 'south$', 'debug_toolbar$', 'crequest$', 'admin$',
    'management$')

INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'crequest.middleware.CrequestMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar', )
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }

AUTHENTICATION_BACKENDS = (
    'core.backends.CASBackend',
)


# Set ID for flatpages
SITE_ID = 1  # REQUIRED FOR 'django.contrib.flatpages'


# Authentication CAS - ULL

CAS_SERVER_URL = 'https://loginpruebas.ull.es/cas-1/'
# The URL prefix of the Django administration site.
CAS_ADMIN_PREFIX = 'admin'
# Extra URL parameters to add to the login URL when redirecting the user
CAS_EXTRA_LOGIN_PARAMS = ''
# If `True`, logging out of the application will always send the user
# to the URL specified by `CAS_REDIRECT_URL`.
CAS_IGNORE_REFERER = False
# If `False`, logging out of the application won't log the user out
# of CAS as well.
CAS_LOGOUT_COMPLETELY = True
# Where to send a user after logging in or out if there is no referrer
# and no next page set. Default is `/`.
CAS_REDIRECT_URL = '/investigacion/'
# If `True` and an unknown or invalid ticket is received,
# the user is redirected back to the login page.
CAS_RETRY_LOGIN = True
#  The CAS protocol version to use.
# `'1'` and `'2'` are supported, with `'2'` being the default.
CAS_VERSION = 'CAS_2_SAML_1_0'
CAS_GRUPOS_NOAUT = ['INSTITUCIONAL']

# Dirección de login para el decorador login_required
LOGIN_URL = 'login'

ROOT_URLCONF = 'investigacion.urls'

WSGI_APPLICATION = 'investigacion.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'memviinv',
        'USER': 'viinv',
        'PASSWORD': '1234',
        'HOST': '',
        'PORT': '',
    },
}

# Internationalization
LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'Atlantic/Canary'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_TEST_URL = '/media_tests/'
MEDIA_TEST_ROOT = os.path.join(BASE_DIR, 'media_tests')

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

WS_SERVER_URL = 'http://django1-pre.stic.ull.es/odin/core/rest/'

LOG_FILENAME = os.path.join(PROJECT_ROOT, 'cvn.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s \
                       <%(pathname)> --- %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
        'standard': {
            'format': '[%(levelname)s] %(asctime)s --- %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        # NullHandler, which will pass any DEBUG (or higher)
        # message to /dev/null.
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        # StreamHandler, which will print any DEBUG (or higher)
        #  message to stderr.
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 4096 * 1024 * 1024,        # 4MB para rotar de fichero
            'backupCount': 5,
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 4096 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',             # Errores de la serie 5XX
            'filters': ['require_debug_false'],  # Only if DEBUG=False
            'class': 'django.utils.log.AdminEmailHandler',
            # Incluye la petición y la traza del error en el mail.
            'include_html': True
        },
        'find_pairs_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'find_pairs.log'
        },
    },
    'loggers': {
        'cvn': {
            'handlers': ['default', 'mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'ERROR',
            'propagate': False
        },
        'cvn.management.commands.find_pairs': {
            'level': 'DEBUG',
            'handlers': ['find_pairs_handler'],
            'propagate': False
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "core.context_processors.external_urls",
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'cvn/templates'),
    os.path.join(BASE_DIR, 'core/templates'),
)

OLD_PORTAL_URL = 'http://aportalpre.stic.ull.es'

# ---------------------------------------------------------- #

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# ---------------------------------------------------------- #

try:
    from settings_local import *
except ImportError:
    pass
