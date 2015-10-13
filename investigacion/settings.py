# -*- encoding: UTF-8 -*-

#
#    Copyright 2014-2015
#
#      STIC-Investigación - Universidad de La Laguna (ULL) <gesinv@ull.edu.es>
#
#    This file is part of Portal del Investigador.
#
#    Portal del Investigador is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    Portal del Investigador is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Portal del Investigador.  If not, see
#    <http://www.gnu.org/licenses/>.
#

import js
import os
from enum import Enum
import csv

# ******************************* PATHS *************************************
# Build paths like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_TEST_ROOT = os.path.join(BASE_DIR, 'media_tests')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
LOG_ROOT = PROJECT_ROOT
# ******************************* PATHS *************************************

# ******************************* URLS **************************************
BASE_URL = 'http://www.example.com'
STATIC_URL = '/investigacion/static/'
MEDIA_URL = '/investigacion/media/'
MEDIA_TEST_URL = '/media_tests/'
TINYMCE_JS_URL = os.path.join(STATIC_URL, 'js/tinymce/resources/tinymce.min.js')
DATATABLES_JS_URL = os.path.join(STATIC_URL, 'js/jquery_datatables/resources/media/js/jquery.dataTables.min.js')
DATATABLES_CSS_URL = os.path.join(STATIC_URL, 'js/jquery_datatables/resources/media/css/jquery.dataTables.min.css')
DATATABLES_SORT_NORMALIZE_URL = os.path.join(STATIC_URL, 'js/jquery_datatables/resources/noaccents.js')
DATATABLES_SORT_DATE_URL = os.path.join(STATIC_URL, 'js/jquery_datatables/resources/date.js')
DATATABLES_SORT_PERCENT_URL = os.path.join(STATIC_URL, 'js/jquery_datatables/resources/percent.js')
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
    ('es', u'Español'),
    ('en', u'English'),
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
    'django.contrib.flatpages',
    'constance',
    'constance.backends.database',
    'logentry_admin',
    'localflavor',
    'impersonate'
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
    'impersonate.middleware.ImpersonateMiddleware'
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
LOGIN_URL = 'login'  # Login address for login_required decorator
LOGOUT_URL = 'logout'
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

DATABASE_ROUTERS = ['core.routers.DynamicDbRouter']

# ******************************* DATABASES *********************************

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

COVERAGE_MODULE_EXCLUDES = (
    'tests$', 'settings$', 'urls$', 'locale$', 'common.views.test', '__init__',
    'django', 'migrations', 'south$', 'debug_toolbar$', 'crequest$', 'admin$',
    'management$')


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
    "constance.context_processors.config",
    "core.context_processors.extra_info",
    "cvn.context_processors.extra_info",
    "core.context_processors.installed_apps",
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# ************************* TEMPLATES ****************************************

# ************************* STATIC FILES *************************************
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'core/static'),
    ('js', js.__path__[0] + ''),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# ************************* STATIC FILES *************************************

# ************************* WEB SERVICES *************************************
WS_SERVER_URL_v1 = 'http://www.example.com/'
WS_SERVER_URL_v2 = 'http://www.example.com/'
# ************************* WEB SERVICES *************************************

# ************************* REDIS ********************************************
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None
REDIS_TIMEOUT = 86400  # One Day (Seconds)
# ************************* REDIS ********************************************

# ************************* OUTPUT *******************************************
CSV_DIALECT = 'investigacion'
csv.register_dialect(unicode(CSV_DIALECT), delimiter='|')
MIMETYPES = {'csv': 'text/csv', 'pdf': 'application/pdf'}
# ************************* OUTPUT *******************************************

# ************************* EMAIL ********************************************
import socket
EMAIL_SUBJECT_PREFIX = "investigacion@" + socket.gethostname() + ": "
SERVER_EMAIL = "investigacion@" + socket.getfqdn(socket.gethostname())

# ************************* EMAIL ********************************************

# ************************* CONSTANCE ****************************************
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_DATABASE_PREFIX = 'constance:investigacion:'
CONSTANCE_CONFIG = {}
CONSTANCE_SUPERUSER_ONLY = False
# ************************* CONSTANCE ****************************************

# ************************ IMPERSONATE ***************************************
IMPERSONATE_REQUIRE_SUPERUSER = True
# ************************ IMPERSONATE ***************************************

# ************************* SETTINGS LOCAL ***********************************
try:
    SETTINGS_LOCAL
except NameError:
    try:
        from .settings_local import *
    except ImportError:
        pass
# ************************* SETTINGS LOCAL ***********************************

# ******************************* LOGGING ************************************
LOG_FILENAME = os.path.join(LOG_ROOT, 'investigacion.log')
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
        'cvn.reports.reports': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}
# ******************************* LOGGING ************************************

# ************************* WEB SERVICES *************************************


class WS_RESULT_CODE(Enum):
    OK = u"OK"
    ERROR = u"ERROR"

# All categories. This is used only on the statistics app.
# There is no need to provide this WS if the statistics app is not being used.
WS_CCE = WS_SERVER_URL_v1 + 'get_cce?past_days=%s'

# RRHH code
WS_COD_PERSONA = WS_SERVER_URL_v1 + 'get_codpersona?nif=%s'
# Document
WS_DOCUMENT = WS_SERVER_URL_v2 + 'uxxirh/persona/%s/numero_documento/'


# CVN Info ULL: learning_degree / learning_phd
WS_ULL_LEARNING = WS_SERVER_URL_v2 + 'uxxirh/persona/%s/titulacion/'

# CVN Info ULL: profession / old_profession
WS_ULL_CARGOS = WS_SERVER_URL_v2 + 'uxxirh/persona/%s/cargo/'
WS_ULL_CONTRATOS = WS_SERVER_URL_v2 + 'uxxirh/persona/%s/contrato/'

# CVN Info ULL: teaching
WS_ULL_TEACHING = WS_SERVER_URL_v1 + 'get_docencia?cod_persona=%s'

# All current departments and members
WS_DEPARTMENTS_AND_MEMBERS = (
    WS_SERVER_URL_v1 +
    'get_departamentos_y_ultimos_miembros')

# All departments and members by years
WS_DEPARTMENTS_AND_MEMBERS_YEAR = (
    WS_SERVER_URL_v1 +
    'get_departamentos_y_ultimos_miembros?year=%s')

# Current department and members of an user
WS_DEPARTMENTS_AND_MEMBERS_USER = (
    WS_SERVER_URL_v1 +
    'get_departamentos_y_ultimos_miembros?cod_persona=%s')

# Department and members of an user by years
WS_DEPARTMENTS_AND_MEMBERS_USER_YEAR = (
    WS_SERVER_URL_v1 +
    'get_departamentos_y_ultimos_miembros?cod_persona=%s&year=%s')

# Info and members of a department
WS_DEPARTMENTS_AND_MEMBERS_UNIT = (
    WS_SERVER_URL_v1 +
    'get_departamentos_y_ultimos_miembros?codigo=%s')

# Info and members of a department by years
WS_DEPARTMENTS_AND_MEMBERS_UNIT_YEAR = (
    WS_SERVER_URL_v1 +
    'get_departamentos_y_ultimos_miembros?codigo=%s&year=%s')

# List of departments that ever existed
WS_DEPARTMENTS_ALL = WS_SERVER_URL_v1 + 'get_departamentos'
WS_DEPARTMENTS_BY_YEAR = WS_SERVER_URL_v1 + 'get_departamentos?year=%s'

# All current areas and members
WS_AREAS_AND_MEMBERS = (
    WS_SERVER_URL_v1 +
    'get_areas_y_ultimos_miembros')

# All areas and members by years
WS_AREAS_AND_MEMBERS_YEAR = (
    WS_SERVER_URL_v1 +
    'get_areas_y_ultimos_miembros?year=%s')

# Current area and members of an user
WS_AREAS_AND_MEMBERS_USER = (
    WS_SERVER_URL_v1 +
    'get_areas_y_ultimos_miembros?cod_persona=%s')

# Area and members of an user by years
WS_AREAS_AND_MEMBERS_USER_YEAR = (
    WS_SERVER_URL_v1 +
    'get_areas_y_ultimos_miembros?cod_persona=%s&year=%s')

# Info and members of an area
WS_AREAS_AND_MEMBERS_UNIT = (
    WS_SERVER_URL_v1 +
    'get_areas_y_ultimos_miembros?codigo=%s')

# Info and members of an area by years
WS_AREAS_AND_MEMBERS_UNIT_YEAR = (
    WS_SERVER_URL_v1 +
    'get_areas_y_ultimos_miembros?codigo=%s&year=%s')

# List of all areas that ever existed
WS_AREAS_ALL = WS_SERVER_URL_v1 + 'get_areas'
WS_AREAS_BY_YEAR = WS_SERVER_URL_v1 + 'get_areas?year=%s'

# This is used only on the accounting app.
# There is no need to provide this WS if the statistics app is not being used.
WS_DETALLES = WS_SERVER_URL_v1 + 'get_detalles?cod_organica=%s'
WS_DESGLOSE_YEAR = WS_SERVER_URL_v1 + 'get_desglose_anyos?cod_organica=%s'
WS_RESUMEN_CONCEPTO = WS_SERVER_URL_v1 + 'get_resumen_concepto?cod_organica=%s'
WS_RESUMEN_YEAR = WS_SERVER_URL_v1 + 'get_resumen_anyos?cod_organica=%s'
# ****************************** WEB SERVICES ******************************
