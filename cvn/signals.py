# -*- encoding: UTF-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, pre_delete
from models import CVN
from core import settings as st_core
from cvn import settings as st_cvn
from core.models import Log
import datetime


# Admin actions not calling model's delete() method
# https://code.djangoproject.com/ticket/10751
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
