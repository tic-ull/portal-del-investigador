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
    message = models.TextField(u'Mensaje')

    def __unicode__(self):
        return u'%s - %s' % (self.application,
                             stCore.TYPE_STATES[self.entry_type][1])

    class Meta:
        ordering = ['-date']
