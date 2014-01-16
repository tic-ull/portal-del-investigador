# -*- encoding: utf-8 -*-
# Django settings for ViinV project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('STIC-Investigacion', 'stic.investigacion@ull.es'),
)
MANAGERS = ADMINS

#~ DATABASES = {
    #~ 'default': {
        #~ 'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        #~ 'NAME': 'memviinv'           ,                      # Or path to database file if using sqlite3.
        #~ # The following settings are not used with sqlite3:
        #~ 'USER': 'viinv',
        #~ 'PASSWORD': '1234',
        #~ 'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        #~ 'PORT': '',                      # Set to empty string for default.
    #~ },
    #~ 'portalinvestigador': {
        #~ 'ENGINE': 'django.db.backends.mysql', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #~ 'NAME': 'portalinvestigador',         # Or path to database file if using sqlite3.
        #~ 'USER': 'root',                       # Not used with sqlite3.
        #~ 'PASSWORD': '1234',                 # Not used with sqlite3.
        #~ 'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
    #~ }
#~ }

# WARNING
# Las bases de datos se cambiaron para apuntar a la copia "frozen" de la Memoria 2012

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'memviinv',
        'USER': 'viinv',
        'PASSWORD': '1234',
        'HOST': '',
        'PORT': '',
    },
    'portalinvestigador': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portalinvestigador',
        'USER': 'root',
        'PASSWORD': '1234',
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
    },

    # db alias for MEMORIA 2012
    'mem2012_db_alias': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'memviinv12',
        'USER': 'root',
        'PASSWORD': '1234',
    }

}

DATABASE_ROUTERS = ['viinvDB.router.viinvRouter', 'cvn.router.cvnRouter']

# Configuracion del logging
LOG_FILENAME = os.path.join(PROJECT_ROOT, 'cvn.log')

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Atlantic/Canary'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-Es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z7(##tnkvh@@h@rcpcu+&v=nyy!(nt1y6a8ovb5l7yk04bxh3+'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # NOTE situado en el 'settings_local'
    #~ 'django_cas.middleware.CASMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)

ROOT_URLCONF = 'ViinV.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ViinV.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    #~ os.path.join(PROJECT_ROOT,'../templates'),

    os.path.join(BASE_DIR, 'templates'),

)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # Extensiones
    'django_extensions',
    'south',
    # Migraciones del modelo
    # Aplicaciones del proyecto
    'cvn',
    # BBDD de Viinv
    'viinvDB',
    # Bootstrap
    'bootstrap_toolkit',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
            'maxBytes': 4096*1024*1024,        # 4MB para rotar de fichero
            'backupCount': 5,
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 4096*1024*1024,
            'backupCount': 5,
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',             # Errores de la serie 5XX
            'filters': ['require_debug_false'],  # Only if DEBUG=False
            'class': 'django.utils.log.AdminEmailHandler',
            # Incluye la petición y la traza del error en el mail.
            'include_html': True
        }
    },
    'loggers': {
        'cvn': {
            'handlers': ['default', 'mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
        # Logs de la plantilla de ADMIN
        # TODO: Ver si es mejor cambiar el 'handler'
        'viinvDB.admin': {
            'handlers': ['default', 'mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'ERROR',
            'propagate': False
        },
    }
}


# Autentificación CAS
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

# Lanzar tests sin usar las migraciones de South
SOUTH_TESTS_MIGRATE = False  # To disable migrations and use syncdb instead
SKIP_SOUTH_TESTS = True     # To disable South's own unit tests

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'cvn/tests/fixtures/'),
)

try:
    execfile(os.path.join(PROJECT_ROOT, 'settings_local.py'))
except IOError:
    pass
