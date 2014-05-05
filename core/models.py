# -*- encoding: UTF-8 -*-

from core import settings as stCore
from cvn.parser_helpers import parse_nif
from django.contrib.auth.models import User
from django.db import models
from lxml import etree


class UserProfile(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#IDENTIFICACION
    """
    user = models.OneToOneField(User, related_name='profile')
    documento = models.CharField(u'Documento', max_length=20,
                                 blank=True, null=True, unique=True)
    rrhh_code = models.CharField(u'Código persona', max_length=20,
                                 blank=True, null=True, unique=True)

    def __unicode__(self):
        return self.user.username

    def can_upload_cvn(self, xml):
        xml_tree = etree.XML(xml)
        nif = parse_nif(xml_tree)
        if (self.user.has_perm('can_upload_other_users_cvn') or
           nif.upper() == self.user.profile.documento.upper()):
            return True
        return False


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
