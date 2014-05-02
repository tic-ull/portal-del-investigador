# -*- encoding: UTF-8 -*-

from core import settings as stCore
from cvn.models import UserProfile
from django.db import models


class Log(models.Model):

    user = models.ForeignKey(UserProfile)
    application = models.CharField(u'Aplicación', max_length=20)
    entry_type = models.IntegerField(u'Tipo', max_length=50,
                                  choices=stCore.TYPE_STATES)
    date = models.DateTimeField(u'Fecha')
    message = models.CharField(u'Mensaje', max_length=100)

    def __unicode__(self):
        return "%s %s" % (self.user, self.application)

    class Meta:
        ordering = ['-date']
