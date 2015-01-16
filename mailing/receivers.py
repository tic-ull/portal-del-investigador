# -*- encoding: UTF-8 -*-

from cvn.signals import pre_cvn_status_changed
import cvn.settings as st_cvn
import mailing.settings as st_mail
from .send_mail import send_mail
from django.dispatch import receiver

@receiver(pre_cvn_status_changed)
def send_mail_cvn_expired(cvn, **kwargs):
    if cvn.status == st_cvn.CVNStatus.EXPIRED:
        send_mail(email_type=st_mail.MailType.EXPIRED,
                  user=cvn.user_profile.user,
                  app_label=cvn._meta.app_label)