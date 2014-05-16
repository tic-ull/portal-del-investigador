# -*- encoding: UTF-8 -*-

from core import settings as stCore
from django.contrib.auth.models import User
from django.db import models
import simplejson as json
from django.conf import settings as st
import urllib


class UserProfile(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#IDENTIFICACION
    """
    user = models.OneToOneField(User, related_name='profile')
    documento = models.CharField(u'Documento', max_length=20, unique=True)
    rrhh_code = models.CharField(u'Código persona', max_length=20,
                                 blank=True, null=True, unique=True)

    def update_rrhh_code(self):
        WS = st.WS_SERVER_URL + 'get_codpersona?nif=' + self.documento
        rrhh_request = urllib.urlopen(WS)
        if rrhh_request.code == 200:
            rrhh_code = rrhh_request.read()
            if rrhh_code.isdigit():
                self.rrhh_code = json.loads(rrhh_code)
        self.save()

    def __unicode__(self):
        return self.user.username


class Log(models.Model):
    user_profile = models.ForeignKey(UserProfile, blank=True, null=True)
    application = models.CharField(u'Aplicación', max_length=20)
    entry_type = models.IntegerField(u'Tipo', choices=stCore.LOG_TYPE)
    date = models.DateTimeField(u'Fecha')
    message = models.TextField(u'Mensaje')

    def __unicode__(self):
        return u'%s - %s' % (self.application,
                             stCore.LOG_TYPE[self.entry_type][1])

    class Meta:
        ordering = ['-date']
