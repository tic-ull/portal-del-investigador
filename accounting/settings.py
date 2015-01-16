# -*- encoding: UTF-8 -*-

SIGIDI_DB = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'name',
    'USER': 'user',
    'PASSWORD': 'password',
    'HOST': '',
    'PORT': '',
}

# ************************* SETTINGS LOCAL ***********************************
try:
    ACCOUNTING_SETTINGS_LOCAL
except NameError:
    try:
        from .settings_local import *
    except ImportError:
        pass
# ************************* SETTINGS LOCAL ***********************************