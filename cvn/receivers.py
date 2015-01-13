# -*- encoding: UTF-8 -*-

from core import settings as st_core
from core.models import Log
from cvn import settings as st_cvn
from cvn import signals
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, pre_delete
from models import CVN, OldCvnPdf

import datetime
import json


# Admin actions not calling model's delete() method
# https://code.djangoproject.com/ticket/10751
def cvn_delete_files(sender, instance, **kwargs):
    instance.cvn_file.delete(False)
    if hasattr(instance, 'xml_file'):
        instance.xml_file.delete(False)

pre_delete.connect(cvn_delete_files, sender=CVN)
pre_delete.connect(cvn_delete_files, sender=OldCvnPdf)


def log_status_cvn_changed(sender, instance, **kwargs):
    try:
        old_status = instance.__class__.objects.get(pk=instance.pk).status
    except ObjectDoesNotExist:
        # old_status = updated so the first time a user uploads a cvn, if it
        # is expired it will be considered a status change
        old_status = st_cvn.CVNStatus.UPDATED
    date_format = '%d/%m/%Y'
    Log.objects.create(
        user_profile=instance.user_profile,
        application=instance._meta.app_label.upper(),
        entry_type=st_core.LogType.CVN_UPDATED,
        date=datetime.datetime.now(),
        message=json.dumps({
            'status': st_cvn.CVN_STATUS[instance.status][1],
            'fecha': instance.fecha.strftime(date_format),
            'uploaded_at': instance.uploaded_at.strftime(date_format)
        })
    )
    if instance.status != old_status:
        signals.cvn_status_changed.send(sender=instance)

pre_save.connect(log_status_cvn_changed, sender=CVN,
                 dispatch_uid='log_status_cvn_changed')
