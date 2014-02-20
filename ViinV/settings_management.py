# -*- encoding: utf-8 -*-

import os
try:
    execfile(os.path.join(PROJECT_ROOT, 'settings.py'))
except IOError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'investigacion_2012',
        'USER': 'investigacion',
        'PASSWORD': 'netUf0Quigak',
        'HOST': 'django1-pre.stic.ull.es'
    },
    'portalinvestigador': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portalinvestigador',
        'USER': 'root',
        'PASSWORD': '1234',
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
    },
    # DB Cleaning
    'historica': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'investigacion_2012',
        'USER': 'investigacion',
        'PASSWORD': 'netUf0Quigak',
        'HOST': 'django1-pre.stic.ull.es'
    }
}
