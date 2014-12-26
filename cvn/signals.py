# -*- encoding: UTF-8 -*-

from core import settings as st_core
from core.models import Log
from cvn import settings as st_cvn
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, pre_delete
from mailing import settings as st_mail
from mailing.send_mail import send_mail
from models import CVN, OldCvnPdf

import datetime


# Admin actions not calling model's delete() method
# https://code.djangoproject.com/ticket/10751
def cvn_delete_files(sender, instance, **kwargs):
    instance.cvn_file.delete(False)
    if hasattr(instance, 'xml_file'):
        instance.xml_file.delete(False)

pre_delete.connect(cvn_delete_files, sender=CVN)
pre_delete.connect(cvn_delete_files, sender=OldCvnPdf)


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
        if instance.status == st_cvn.CVNStatus.EXPIRED:
            send_mail(email_type=st_mail.MailType.EXPIRED,
                      user=instance.user_profile.user,
                      app_label=instance._meta.app_label)

pre_save.connect(log_status_cvn_changed, sender=CVN,
                 dispatch_uid='log_status_cvn_changed')
