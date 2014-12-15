# -*- encoding: UTF-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, pre_delete
from models import Proyecto, Convenio, CVN
from core import settings as st_core
from cvn import settings as st_cvn
from core.models import Log
import datetime


def save_date(sender, instance, **kwargs):
    try:
        db_instance = instance.__class__.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return
    if (not hasattr(db_instance, 'fecha_de_fin') or
            not hasattr(db_instance, 'duracion')):
        return
    if (db_instance.fecha_de_fin != instance.fecha_de_fin and
       instance.fecha_de_fin is not None):
        duracion = instance.fecha_de_fin - instance.fecha_de_inicio
        instance.duracion = duracion.days
    elif (db_instance.duracion != instance.duracion and
            instance.duracion is not None):
        instance.fecha_de_fin = (instance.fecha_de_inicio +
                                 datetime.timedelta(days=instance.duracion))

pre_save.connect(save_date, sender=Proyecto, dispatch_uid='save-date')
pre_save.connect(save_date, sender=Convenio, dispatch_uid='save-date')


def cvn_delete_files(sender, instance, **kwargs):
    instance.cvn_file.delete(False)
    instance.xml_file.delete(False)

pre_delete.connect(cvn_delete_files, sender=CVN)


def log_status_cvn_changed(sender, instance, **kwargs):
    updated = False
    try:
        db_instance = instance.__class__.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        updated = True
    else:
        if instance.status != db_instance.status:
            updated = True

    if updated:
        Log.objects.create(
            user_profile=instance.user_profile,
            application=instance._meta.app_label.upper(),
            entry_type=st_core.LogType.CVN_STATUS,
            date=datetime.datetime.now(),
            message=st_cvn.CVN_STATUS[instance.status][1]
        )

pre_save.connect(log_status_cvn_changed, sender=CVN,
                 dispatch_uid='log_status_cvn_changed')