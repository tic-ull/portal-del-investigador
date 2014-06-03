# -*- encoding: UTF-8 -*-

from core import settings as stCore
from django.conf import settings as st
from django.contrib.auth.models import User
from django.db import models
import simplejson as json
from django.utils.translation import ugettext_lazy as _
import urllib


class UserProfile(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#IDENTIFICACION
    """
    user = models.OneToOneField(User, related_name='profile')
    documento = models.CharField(_('Documento'), max_length=20, unique=True)
    rrhh_code = models.CharField(_(u'Código persona'), max_length=20,
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
    application = models.CharField(_(u'Aplicación'), max_length=20)
    entry_type = models.IntegerField(_('Tipo'), choices=stCore.LOG_TYPE)
    date = models.DateTimeField(_('Fecha'))
    message = models.TextField(_('Mensaje'))

    def __unicode__(self):
        return u'%s - %s' % (self.application,
                             stCore.LOG_TYPE[self.entry_type][1])

    class Meta:
        ordering = ['-date']
