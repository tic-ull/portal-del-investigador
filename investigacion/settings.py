# -*- encoding: UTF-8 -*-

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
BASE_URL = 'http://wwwpre.ull.es/portaldeinvestigacion'
STATIC_URL = '/investigacion/static/'
MEDIA_URL = '/investigacion/media/'
MEDIA_TEST_URL = '/media_tests/'
LOGIN_URL = 'login'  # Login address for login_required decorator
TINYMCE_JS_URL = os.path.join(STATIC_URL, 'tiny_mce/tiny_mce.js')
TINYMCE_JS_TEXTAREA = os.path.join(STATIC_URL, 'tiny_mce/conf/textarea.js')
OLD_PORTAL_URL = 'http://aportalpre.stic.ull.es'
# ******************************* URLS **************************************

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z7(##tnkvh@@h@rcpcu+&v=nyy!(nt1y6a8ovb5l7yk04bxh3+'

# Enable translation of strings in this file
_ = lambda s: s

# ******************************* ADMINS *************************************
ADMINS = (
    ('STIC-Investigacion', 'stic.investigacion@ull.es'),
)
MANAGERS = ADMINS
# ******************************* ADMINS *************************************

# ******************************* LANGUAGE ***********************************
LANGUAGES = (
    ('es', 'Español'),
    ('en', 'English'),
)
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'es'
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'core/locale'),
    os.path.join(BASE_DIR, 'cvn/locale'),
    os.path.join(BASE_DIR, 'statistics/locale'),
    os.path.join(BASE_DIR, 'accounting/locale'),
)
TIME_ZONE = 'Atlantic/Canary'
USE_TZ = True
# ******************************* LANGUAGE ***********************************

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django.contrib.sites',
    'tinymce',
    'south',
    'core',
    'cvn',
    'crequest',
    'statistics',
    'django_coverage',
    'django_tables2',
    'mptt',
    'modeltranslation',
    'flatpages_i18n',
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
    'django.middleware.locale.LocaleMiddleware',
    'crequest.middleware.CrequestMiddleware',
    'flatpages_i18n.middleware.FlatpageFallbackMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'core.backends.CASBackend',
)

# Development and debugging configuration
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEVEL = True

# Set ID for flatpages
SITE_ID = 1  # REQUIRED FOR 'django.contrib.flatpages'

# ************************* AUTHENTICATION CAS - ULL *************************
CAS_SERVER_URL = 'https://loginpruebas.ull.es/cas-1/'
CAS_ADMIN_PREFIX = 'admin'  # The URL prefix of the Django administration site
CAS_EXTRA_LOGIN_PARAMS = ''  # Extra parameters for login URL when redirecting
CAS_IGNORE_REFERER = False
CAS_LOGOUT_COMPLETELY = True
CAS_REDIRECT_URL = '/investigacion/'  # Redirect here when no referrer
CAS_RETRY_LOGIN = True
CAS_VERSION = 'CAS_2_SAML_1_0'
CAS_GRUPOS_NOAUT = ['INSTITUCIONAL']
# ************************* AUTHENTICATION CAS - ULL *************************

ROOT_URLCONF = 'investigacion.urls'

WSGI_APPLICATION = 'investigacion.wsgi.application'

# ******************************* DATABASES *********************************
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'memviinv',
        'USER': '<user>',
        'PASSWORD': '<password>',
        'HOST': '',
        'PORT': '',
    },
}

SIGIDI_DB = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': '<name>',
    'USER': '<user>',
    'PASSWORD': '<password>',
    'HOST': '',
    'PORT': '',
}
# ******************************* DATABASES *********************************

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

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
            'handlers': ['request_handler'],
            'level': 'ERROR',
            'propagate': False,
        },
        'default': {
            'handlers': ['default', 'mail_admins'],
            'propagate': True,
        },
        'cvn': {
            'handlers': ['default'],
            'propagate': True,
        },
        'cvn.management.commands.find_pairs': {
            'handlers': ['find_pairs_handler'],
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
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'cvn/templates'),
    os.path.join(BASE_DIR, 'core/templates'),
    os.path.join(BASE_DIR, 'statistics/templates'),
    os.path.join(BASE_DIR, 'accounting/templates'),
)
# ************************* TEMPLATES ****************************************

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# ************************* WEB SERVICES *************************************
WS_SERVER_URL = 'http://django1-pre.stic.ull.es/odin/core/rest/'
# ************************* WEB SERVICES *************************************

# ************************* REDIS ********************************************
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None
REDIS_TIMEOUT = 86400  # One Day (Seconds)
# ************************* REDIS ********************************************

# ************************* SETTINGS LOCAL ***********************************
try:
    SETTINGS_LOCAL
except NameError:
    try:
        from settings_local import *
    except ImportError:
        pass
# ************************* SETTINGS LOCAL ***********************************

# ************************* WEB SERVICES *************************************
# All categories
WS_CCE = WS_SERVER_URL + 'get_cce?past_days=%s'

# RRHH code
WS_COD_PERSONA = WS_SERVER_URL + 'get_codpersona?nif=%s'

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
# ************************* WEB SERVICES *************************************
