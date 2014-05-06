# -*- encoding: UTF-8 -*-

from core import settings as stCore
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#IDENTIFICACION
    """
    user = models.OneToOneField(User, related_name='profile')
    documento = models.CharField(u'Documento', max_length=20, unique=True)
    rrhh_code = models.CharField(u'Código persona', max_length=20,
                                 blank=True, null=True, unique=True)

    def __unicode__(self):
        return self.user.username


class Log(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    application = models.CharField(u'Aplicación', max_length=20)
    entry_type = models.IntegerField(u'Tipo', max_length=50,
                                     choices=stCore.LOG_TYPE)
    entry_type = models.IntegerField(u'Tipo', choices=stCore.LOG_TYPE,
                                     default=0)
    date = models.DateTimeField(u'Fecha')
    message = models.TextField(u'Mensaje')

    def __unicode__(self):
        return u'%s - %s' % (self.application,
                             stCore.LOG_TYPE[self.entry_type][1])

    class Meta:
        ordering = ['-date']
