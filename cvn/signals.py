from django.db.models.signals import post_save
from cvn.models import Usuario
from django.contrib.auth.models import User


def create_profile(sender, instance, created, **kwargs):
    usuario = Usuario.objects.filter(user__username=instance.username)
    if created and (len(usuario) == 0):
        usuario = Usuario()
        usuario.user = instance
        usuario.save()

post_save.connect(create_profile, sender=User,
                  dispatch_uid="signal-create-profile")
