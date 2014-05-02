# -*- encoding: UTF-8 -*-

from crequest.middleware import CrequestMiddleware
from cvn.models import UserProfile, Proyecto, Convenio
from django.conf import settings as st
from django.contrib.auth.models import User  # , Permission
from django.db.models.signals import post_save, pre_save  # , post_syncdb
from django.core.exceptions import ObjectDoesNotExist
import datetime
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


def save_date(sender, instance, **kwargs):
    try:
        db_instance = instance.__class__.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return
    if (not hasattr(db_instance, 'fecha_de_fin') or
            not hasattr(db_instance, 'duracion')):
        return
    if db_instance.fecha_de_fin != instance.fecha_de_fin:
        duracion = instance.fecha_de_fin - instance.fecha_de_inicio
        instance.duracion = duracion.days
    elif db_instance.duracion != instance.duracion:
        instance.fecha_de_fin = (instance.fecha_de_inicio +
                                 datetime.timedelta(days=instance.duracion))

pre_save.connect(save_date, sender=Proyecto, dispatch_uid='save-date')
pre_save.connect(save_date, sender=Convenio, dispatch_uid='save-date')
