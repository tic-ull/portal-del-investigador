# -*- encoding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
import mailing.settings as st_mail

class Email(models.Model):
    entry_type = models.IntegerField(_('Tipo'), choices=st_mail.MAIL_TYPE,
                                     null=False)
    title = models.CharField(_(u'Título'), max_length=255, blank=False)
    content = models.TextField(_('Contenido'), blank=False)

    def __unicode__(self):
        return st_mail.MailType(self.entry_type).name