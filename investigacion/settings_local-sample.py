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

SETTINGS_LOCAL = True
from .settings import *

# PATHS
LOG_ROOT = '/tmp/'

# URLS
BASE_URL = 'http://example.com'
OLD_PORTAL_URL = 'http://example.com'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret_key-sample'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
DEVEL = True

# ADMINS
ADMINS = (
    ('STIC-Investigacion', 'email@example.com'),
)
MANAGERS = ADMINS

SUPPORT = u'Servicio de Investigación'
EMAIL_SUPPORT = 'email@example.com'

# Enable ROSETTA
"""
INSTALLED_APPS = ('rosetta', ) + INSTALLED_APPS
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'core/locale'),
    os.path.join(BASE_DIR, 'cvn/locale'),
    os.path.join(BASE_DIR, 'statistics/locale'),
    os.path.join(BASE_DIR, 'accounting/locale'),
    os.path.join(BASE_DIR, 'mailing/locale'),
)
"""

# Enable DJANGO DEBUG TOOLBAR
"""
INSTALLED_APPS = ('debug_toolbar', ) + INSTALLED_APPS
DEBUG_TOOLBAR_PATCH_SETTINGS = False
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }
"""

# AUTHENTICATION CAS
CAS_SERVER_URL = 'http://www.example.com/cas-1/'

# WEB SERVICES
WS_SERVER_URL_v1 = 'http://www.example.com/'
WS_SERVER_URL_v2 = 'http://www.example.com/'

# Proprietary applications
# INSTALLED_APPS = INSTALLED_APPS + ('statistics', 'accounting', 'mailing')

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<default_name>',
        'USER': '<default_user>',
        'PASSWORD': '<default_password>',
        'HOST': '<default_host',
        'PORT': '<default_port>',
    },
    '2013': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<2013_name>',
        'USER': '<2013_user>',
        'PASSWORD': '<2013_password>',
        'HOST': '<2013_host>',
        'PORT': '<2013_port>',
    },
    '2014': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<2014_name>',
        'USER': '<2014_user>',
        'PASSWORD': '<2014_password>',
        'HOST': '<2014_host>',
        'PORT': '<2014_port>',
    },
    # You can define more historical databases here.
}
