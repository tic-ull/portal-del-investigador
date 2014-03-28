from django.db.models.signals import post_save, post_syncdb
from cvn.models import Usuario
from django.contrib.auth.models import User, Permission
from crequest.middleware import CrequestMiddleware
from django.db import connection
import logging


def create_profile(sender, instance, created, **kwargs):
    # La siguiente linea se puede eliminar cuando se quite viinvdb
    usuario = Usuario.objects.filter(user__username=instance.username)
    if created and (len(usuario) == 0):
        cas_info = CrequestMiddleware.get_request().session['attributes']
        usuario = Usuario()
        usuario.user = instance
        usuario.documento = cas_info['NumDocumento']
        usuario.save()

post_save.connect(create_profile, sender=User,
                  dispatch_uid="signal-create-profile")


# Related ticket http://code.djangoproject.com/ticket/4748
def alter_django_auth_permissions(sender, **kwargs):
    logger = logging.getLogger(__name__)
    if not Permission in kwargs['created_models']:
        return
    SIZE_NAME = 128
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM auth_permission LIMIT 1")

    for desc in cursor.description:
        # See http://www.python.org/dev/peps/pep-0249/
        (name, type_code, display_size, internal_size, precision,
         scale, null_ok) = desc
        if not name == 'name':
            continue
        if internal_size < SIZE_NAME:
            logger.info('auth_permission: Column "name" gets altered.\
                         Old: %d new: %d' % (internal_size, SIZE_NAME))
            cursor.execute('''ALTER TABLE auth_permission ALTER COLUMN\
                           "name" type VARCHAR(%s)''',
                           [SIZE_NAME])
        break
    else:
        raise Exception('table auth_permission has not column "name"')

post_syncdb.connect(alter_django_auth_permissions)
