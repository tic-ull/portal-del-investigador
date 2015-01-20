# -*- encoding: UTF-8 -*-

SETTINGS_LOCAL = True
from .settings import *

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
WS_SERVER_URL = 'http://www.example.com/'

# Proprietary applications
# INSTALLED_APPS = INSTALLED_APPS + ('statistics', 'accounting', 'mailing')

# DATABASES
DATABASES['default']['NAME'] = 'name'
DATABASES['default']['USER'] = 'user'
DATABASES['default']['PASSWORD'] = 'password'
DATABASES['default']['HOST'] = 'localhost'

DATABASES['historica_2013'] = DATABASES['default'].copy()
DATABASES['historica_2013']['TEST_MIRROR'] = 'default'
DATABASES['historica_2013']['OPTIONS'] = {
    'options': '-c search_path=schema_2013'
}

HISTORICAL = {
    '2013': 'historica_2013',
}
