# -*- encoding: UTF-8 -*-

from core import settings as st_core
from django.conf import settings as st
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ws_utils import CachedWS as ws
import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    documento = models.CharField(_('Documento'), max_length=20, unique=True)

    rrhh_code = models.CharField(_(u'Código persona'), max_length=20,
                                 blank=True, null=True, unique=True)

    @classmethod
    def get_or_create_user(cls, username, documento):
        created = False
        try:
            user = User.objects.get(profile__documento=documento)
        except User.DoesNotExist:
            user, created = User.objects.get_or_create(username=username)
            if created:
                profile = cls.objects.create(user=user, documento=documento)
                profile.update_rrhh_code()
            else:
                Log.objects.create(
                    user_profile=user.profile,
                    application='core',
                    entry_type=st_core.LogType.AUTH_ERROR,
                    date=datetime.datetime.now(),
                    message='Username already exists. Possibly changed ID.' +
                            ' Old ID = ' + user.profile.documento +
                            ' New ID = ' + documento)

        return user, created

    def update_rrhh_code(self):
        rrhh_code = ws.get(ws=(st.WS_COD_PERSONA % self.documento),
                           use_redis=False)
        if rrhh_code is not None:
            self.rrhh_code = rrhh_code
            self.save()

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ['user__username']


class Log(models.Model):
    user_profile = models.ForeignKey(UserProfile, blank=True, null=True)

    application = models.CharField(_(u'Aplicación'), max_length=20)

    entry_type = models.IntegerField(_('Tipo'), choices=st_core.LOG_TYPE)

    date = models.DateTimeField(_('Fecha'))

    message = models.TextField(_('Mensaje'))

    def __unicode__(self):
        return u'%s - %s' % (self.application,
                             st_core.LOG_TYPE[self.entry_type][1])

    class Meta:
        ordering = ['-date']
