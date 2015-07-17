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

from core.models import UserProfile
from django.conf import settings as st
from django.contrib.auth.backends import ModelBackend
from django_cas.backends import _verify
import django_cas
from ws_utils import CachedWS as ws
from django.core.exceptions import ObjectDoesNotExist
from .admin_advanced  import change_dni
class CASBackend(django_cas.backends.CASBackend, ModelBackend):

    def authenticate(self, ticket, service, request):
        """Verifies CAS ticket and gets or creates User object"""
        username, attributes = _verify(ticket, service)
        # If we don't have the user's document we'll not allow him to do login
        if (not attributes or not 'NumDocumento' in attributes
                or attributes['NumDocumento'] is None):
            st.CAS_RETRY_LOGIN = False
            return None
        # If type of account of the user isn't allow then
        # we will not allow him to do login
        if (attributes and 'TipoCuenta' in attributes
                and attributes['TipoCuenta'] in st.CAS_TIPO_CUENTA_NOAUT):
            st.CAS_RETRY_LOGIN = False
            return None
        try:
            user = UserProfile.objects.get(user__username=username)
            if attributes['NumDocumento'] != user.documento:
                rrhh_code1 = ws.get(url=(st.WS_COD_PERSONA % attributes['NumDocumento']), use_redis=False)
                rrhh_code2 = ws.get(url=(st.WS_COD_PERSONA % user.documento), use_redis=False)
                if rrhh_code1 == rrhh_code2:
                    change_dni(user, attributes['NumDocumento'])
        except ObjectDoesNotExist:
            pass
        request.session['attributes'] = attributes
        documento = attributes['NumDocumento']
        return UserProfile.get_or_create_user(username, documento)[0]
