from django.db.models.signals import post_save
from cvn.models import Usuario
from django.contrib.auth.models import User
from crequest.middleware import CrequestMiddleware


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
