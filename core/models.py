# -*- encoding: UTF-8 -*-

#
#    Copyright 2014-2015
#
#      STIC-Investigación - Universidad de La Laguna (ULL) <gesinv@ull.edu.es>
#
#    This file is part of Portal del Investigador.
#
#    Portal del Investigador is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    Portal del Investigador is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Portal del Investigador.  If not, see
#    <http://www.gnu.org/licenses/>.
#

from core import settings as st_core
from django.conf import settings as st
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ws_utils import CachedWS as ws
import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    documento = models.CharField(_("Document"), max_length=20, unique=True)

    rrhh_code = models.CharField(_("Person code"), max_length=20,
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
        rrhh_code = ws.get(url=(st.WS_COD_PERSONA % self.documento),
                           use_redis=False)
        if rrhh_code is not None:
            self.rrhh_code = rrhh_code
            self.save()

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ['user__username']
        verbose_name_plural = _("User profiles")


class Log(models.Model):
    user_profile = models.ForeignKey(UserProfile, blank=True, null=True)

    application = models.CharField(_("Application"), max_length=20)

    entry_type = models.IntegerField(_("Type"), choices=st_core.LOG_TYPE)

    date = models.DateTimeField(_("Date"))

    message = models.TextField(_("Message"))

    def __unicode__(self):
        return u'%s - %s' % (self.application,
                             st_core.LOG_TYPE[self.entry_type][1])

    class Meta:
        ordering = ['-date']
