# -*- encoding: UTF-8 -*-

import js
import os

# ******************************* PATHS *************************************
# Build paths like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_TEST_ROOT = os.path.join(BASE_DIR, 'media_tests')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
# ******************************* PATHS *************************************

# ******************************* URLS **************************************
BASE_URL = 'http://www.example.com'
STATIC_URL = '/investigacion/static/'
MEDIA_URL = '/investigacion/media/'
MEDIA_TEST_URL = '/media_tests/'
LOGIN_URL = 'login'  # Login address for login_required decorator
TINYMCE_JS_URL = os.path.join(STATIC_URL, 'js/tinymce/resources/tinymce.min.js')
TINYMCE_JS_TEXTAREA = os.path.join(STATIC_URL, 'js/tinymce/conf/textarea.js')
OLD_PORTAL_URL = 'http://www.example.com'
# ******************************* URLS **************************************

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret_key-sample'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
DEVEL = True

INTERNAL_IPS = ('127.0.0.1',)
ALLOWED_HOSTS = ['*']

# REQUIRED FOR 'django.contrib.flatpages'
SITE_ID = 1

# ******************************* ADMINS *************************************
ADMINS = (
    ('STIC-Investigacion', 'email@example.com'),
)
MANAGERS = ADMINS

SUPPORT = u'Servicio de Investigación'
EMAIL_SUPPORT = 'email@example.com'
# ******************************* ADMINS *************************************

# ******************************* LANGUAGE ***********************************

# Enable translation of strings in this file
_ = lambda s: s

LANGUAGES = (
    ('es', 'Español'),
    ('en', 'English'),
)
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'es'
TIME_ZONE = 'Atlantic/Canary'
USE_TZ = False
# ******************************* LANGUAGE ***********************************

# ******************************* INSTALLED APPS *****************************
INSTALLED_APPS = (
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django.contrib.sites',
    'core',
    'cvn',
    'crequest',
    'django_coverage',
    'django_tables2',
    'django.contrib.flatpages',
)
# ******************************* INSTALLED APPS *****************************

# ******************************* MIDDLEWARES ********************************
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'crequest.middleware.CrequestMiddleware',
)
# ******************************* MIDDLEWARES ********************************

AUTHENTICATION_BACKENDS = (
    'core.backends.CASBackend',
)

# ************************* AUTHENTICATION CAS - ULL *************************
CAS_SERVER_URL = 'http://www.example.com/cas-1/'
CAS_ADMIN_PREFIX = 'admin'  # The URL prefix of the Django administration site
CAS_EXTRA_LOGIN_PARAMS = ''  # Extra parameters for login URL when redirecting
CAS_IGNORE_REFERER = False
CAS_LOGOUT_COMPLETELY = True
CAS_REDIRECT_URL = '/investigacion/'  # Redirect here when no referrer
CAS_RETRY_LOGIN = True
CAS_VERSION = 'CAS_2_SAML_1_0'
CAS_TIPO_CUENTA_NOAUT = ['colectivo', ]
# ************************* AUTHENTICATION CAS - ULL *************************

ROOT_URLCONF = 'investigacion.urls'

WSGI_APPLICATION = 'investigacion.wsgi.application'

# ******************************* DATABASES *********************************
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    },
    'historica': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=schema_historica, public'
        },
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
        'TEST_MIRROR': 'default',
    }
}

HISTORICAL = {
    'year': 'historica',
}

SIGIDI_DB = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'name',
    'USER': 'user',
    'PASSWORD': 'password',
    'HOST': '',
    'PORT': '',
}
# ******************************* DATABASES *********************************

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

COVERAGE_MODULE_EXCLUDES = (
    'tests$', 'settings$', 'urls$', 'locale$', 'common.views.test', '__init__',
    'django', 'migrations', 'south$', 'debug_toolbar$', 'crequest$', 'admin$',
    'management$')

# ******************************* LOGGING ************************************
LOG_FILENAME = os.path.join(PROJECT_ROOT, 'investigacion.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s <%(pathname)s>: %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S',
        },
        'simple': {
            'format': '[%(levelname)s] %(asctime)s: %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 5,
            'formatter': 'simple',
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 5,
            'formatter': 'simple',
        },
        'find_pairs_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, 'find_pairs.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['request_handler', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'default': {
            'handlers': ['default', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cvn': {
            'handlers': ['default', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cvn.management.commands.find_pairs': {
            'handlers': ['find_pairs_handler', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
# ******************************* LOGGING ************************************

# ************************* TEMPLATES ****************************************
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "core.context_processors.extra_info",
    "cvn.context_processors.extra_info",
    "core.context_processors.installed_apps"
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# ************************* TEMPLATES ****************************************

# ************************* STATIC FILES *************************************
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    ('js', js.__path__[0] + ''),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# ************************* STATIC FILES *************************************

# ************************* WEB SERVICES *************************************
WS_SERVER_URL = 'http://www.example.com/'
# ************************* WEB SERVICES *************************************

# ************************* REDIS ********************************************
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None
REDIS_TIMEOUT = 86400  # One Day (Seconds)
# ************************* REDIS ********************************************

# ************************* EMAIL ********************************************
import socket
EMAIL_SUBJECT_PREFIX = "investigacion@" + socket.gethostname() + ": "
SERVER_EMAIL = "investigacion@" + socket.getfqdn(socket.gethostname())

# ************************* EMAIL ********************************************

# ************************* SETTINGS LOCAL ***********************************
try:
    SETTINGS_LOCAL
except NameError:
    try:
        from .settings_local import *
    except ImportError:
        pass
# ************************* SETTINGS LOCAL ***********************************

# ************************* WEB SERVICES *************************************
# All categories
WS_CCE = WS_SERVER_URL + 'get_cce?past_days=%s'

# RRHH code
WS_COD_PERSONA = WS_SERVER_URL + 'get_codpersona?nif=%s'

# CVN Info ULL: learning_degree / learning_phd
WS_ULL_LEARNING = WS_SERVER_URL + 'get_formacion_academica?cod_persona=%s'

# CVN Info ULL: profession / old_profession
WS_ULL_CARGOS = WS_SERVER_URL + 'get_cargos?cod_persona=%s'

# All current departments and members
WS_DEPARTMENTS_AND_MEMBERS = (
    WS_SERVER_URL +
    'get_departamentos_y_ultimos_miembros')

# All departments and members by years
WS_DEPARTMENTS_AND_MEMBERS_YEAR = (
    WS_SERVER_URL +
    'get_departamentos_y_ultimos_miembros?year=%s')

# Current department and members of an user
WS_DEPARTMENTS_AND_MEMBERS_USER = (
    WS_SERVER_URL +
    'get_departamentos_y_ultimos_miembros?cod_persona=%s')

# Department and members of an user by years
WS_DEPARTMENTS_AND_MEMBERS_USER_YEAR = (
    WS_SERVER_URL +
    'get_departamentos_y_ultimos_miembros?cod_persona=%s&year=%s')

# Info and members of a department
WS_DEPARTMENTS_AND_MEMBERS_UNIT = (
    WS_SERVER_URL +
    'get_departamentos_y_ultimos_miembros?codigo=%s')

# Info and members of a department by years
WS_DEPARTMENTS_AND_MEMBERS_UNIT_YEAR = (
    WS_SERVER_URL +
    'get_departamentos_y_ultimos_miembros?codigo=%s&year=%s')

# All current departments
WS_DEPARTMENTS = WS_SERVER_URL + 'get_departamentos'

# All departments by years
WS_DEPARTMENTS_YEAR = WS_SERVER_URL + 'get_departamentos?year=%s'

# All current areas and members
WS_AREAS_AND_MEMBERS = (
    WS_SERVER_URL +
    'get_areas_y_ultimos_miembros')

# All areas and members by years
WS_AREAS_AND_MEMBERS_YEAR = (
    WS_SERVER_URL +
    'get_areas_y_ultimos_miembros?year=%s')

# Current area and members of an user
WS_AREAS_AND_MEMBERS_USER = (
    WS_SERVER_URL +
    'get_areas_y_ultimos_miembros?cod_persona=%s')

# Area and members of an user by years
WS_AREAS_AND_MEMBERS_USER_YEAR = (
    WS_SERVER_URL +
    'get_areas_y_ultimos_miembros?cod_persona=%s&year=%s')

# Info and members of an area
WS_AREAS_AND_MEMBERS_UNIT = (
    WS_SERVER_URL +
    'get_areas_y_ultimos_miembros?codigo=%s')

# Info and members of an area by years
WS_AREAS_AND_MEMBERS_UNIT_YEAR = (
    WS_SERVER_URL +
    'get_areas_y_ultimos_miembros?codigo=%s&year=%s')

# All current areas
WS_AREAS = WS_SERVER_URL + 'get_areas'

# All areas by years
WS_AREAS_YEAR = WS_SERVER_URL + 'get_areas?year=%s'

WS_DETALLES = WS_SERVER_URL + 'get_detalles?cod_organica=%s'
WS_DESGLOSE_YEAR = WS_SERVER_URL + 'get_desglose_anyos?cod_organica=%s'
WS_RESUMEN_CONCEPTO = WS_SERVER_URL + 'get_resumen_concepto?cod_organica=%s'
WS_RESUMEN_YEAR = WS_SERVER_URL + 'get_resumen_anyos?cod_organica=%s'
# ****************************** WEB SERVICES ******************************

