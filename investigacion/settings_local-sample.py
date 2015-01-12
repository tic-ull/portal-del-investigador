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
# INSTALLED_APPS = ('rosetta', ) + INSTALLED_APPS

# Enable DJANGO DEBUG TOOLBAR
# INSTALLED_APPS = ('debug_toolbar', ) + INSTALLED_APPS
# DEBUG_TOOLBAR_PATCH_SETTINGS = False
# MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
# DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }

# AUTHENTICATION CAS
CAS_SERVER_URL = 'http://www.example.com/cas-1/'

# DATABASES
DATABASES['default']['NAME'] = 'name'
DATABASES['default']['USER'] = 'user'
DATABASES['default']['PASSWORD'] = 'password'
DATABASES['default']['HOST'] = 'localhost'
DATABASES['default']['OPTIONS'] = {
    'options': '-c search_path=schema_default, public'
}

DATABASES['historica']['NAME'] = 'name'
DATABASES['historica']['USER'] = 'user'
DATABASES['historica']['PASSWORD'] = 'password'
DATABASES['historica']['HOST'] = 'locahost'
DATABASES['historica']['OPTIONS'] = {
    'options': '-c search_path=schema_historica, public'
}

SIGIDI_DB['NAME'] = 'name'
SIGIDI_DB['USER'] = 'user'
SIGIDI_DB['PASSWORD'] = 'password'
SIGIDI_DB['HOST'] = 'localhost'

# WEB SERVICES
WS_SERVER_URL = 'http://www.example.com/'
