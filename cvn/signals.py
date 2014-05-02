# -*- encoding: UTF-8 -*-

from crequest.middleware import CrequestMiddleware
from cvn.models import UserProfile
from django.conf import settings as st
from django.contrib.auth.models import User  # , Permission
#from django.db import connection
from django.db.models.signals import post_save  # , post_syncdb
#import logging
import simplejson as json
import urllib


def create_profile(sender, instance, created, **kwargs):
    if not created:
        return
    profile = UserProfile.objects.create(user=instance)
    request = CrequestMiddleware.get_request()
    if request and 'attributes' in request.session:
        cas_info = request.session['attributes']
        if 'NumDocumento' in cas_info:
            profile.documento = cas_info['NumDocumento']
            WS = st.WS_SERVER_URL + 'get_codpersona?nif=%s' % (
                cas_info['NumDocumento'])
            if urllib.urlopen(WS).code == 200:
                profile.rrhh_code = json.loads(urllib.urlopen(WS).read())
    profile.save()

post_save.connect(create_profile, sender=User, dispatch_uid="create-profile")


# Related ticket http://code.djangoproject.com/ticket/4748
#def alter_django_auth_permissions(sender, **kwargs):
#    logger = logging.getLogger(__name__)
#    if not Permission in kwargs['created_models']:
#        return
#    SIZE_NAME = 128
#    cursor = connection.cursor()
#    cursor.execute("SELECT * FROM auth_permission LIMIT 1")
#
#    for desc in cursor.description:
#        # See http://www.python.org/dev/peps/pep-0249/
#        (name, type_code, display_size, internal_size, precision,
#         scale, null_ok) = desc
#        if not name == 'name':
#            continue
#        if internal_size < SIZE_NAME:
#            logger.info('auth_permission: Column "name" gets altered.\
#                         Old: %d new: %d' % (internal_size, SIZE_NAME))
#            cursor.execute('''ALTER TABLE auth_permission ALTER COLUMN\
#                           "name" type VARCHAR(%s)''',
#                           [SIZE_NAME])
#        break
#    else:
#        raise Exception('table auth_permission has not column "name"')
#
#post_syncdb.connect(alter_django_auth_permissions)
