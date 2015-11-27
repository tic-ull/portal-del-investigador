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

from django.contrib.auth.signals import user_logged_in
from ws_utils import CachedWS as ws
from django.conf import settings as st
import logging
from impersonate.signals import session_begin, session_end
from django.dispatch import receiver

logger = logging.getLogger('default')

@receiver(session_begin)
def impersonate_update_session(impersonating, request, **kwargs):
    if request and 'attributes' in request.session:
        cas_info = request.session['attributes']
        cas_info['first_name'] = impersonating.first_name
        cas_info['last_name'] = impersonating.last_name


@receiver(session_end)
def impersonate_restore_session(impersonator, request, **kwargs):
    if request and 'attributes' in request.session:
        cas_info = request.session['attributes']
        cas_info['first_name'] = impersonator.first_name
        cas_info['last_name'] = impersonator.last_name


def update_user(user, request, **kwargs):
    if request and 'attributes' in request.session:
        cas_info = request.session['attributes']
        if 'first_name' in cas_info:
            user.first_name = cas_info['first_name']
        if 'last_name' in cas_info:
            user.last_name = cas_info['last_name'][:30]
        if 'email' in cas_info:
            user.email = cas_info['email']
        if 'username' in cas_info:
            user.username = cas_info['username']
        user.save()


def update_dni(user, request, **kwargs):
    if 'attributes' in request.session:
        attributes = request.session['attributes']

        if attributes['NumDocumento'] != user.profile.documento:
            rrhh_code = str(ws.get(url=(st.WS_COD_PERSONA % attributes[
                'NumDocumento']), use_redis=False))
            if rrhh_code == user.profile.rrhh_code:
                user.profile.change_dni(attributes['NumDocumento'])
            else:
                logger.error(
                    u'Usuario detectado con número de documento y código de '
                    u'RRHH diferentes\nUser: %s\nOLD Documento: %s - NEW '
                    u'Documento: %s \n' % (attributes['username'],
                                           user.profile.documento,
                                           attributes['NumDocumento']) +
                    u'OLD RRHH: %s - NEW RRHH: %s\n' % (user.profile.rrhh_code,
                                                        rrhh_code) +
                    u'Es necesario verificar si es la misma persona y '
                    u'unificarlas de forma manual desde la interfaz de '
                    u'administración.'
                )


user_logged_in.connect(update_user, dispatch_uid='update-profile')
user_logged_in.connect(update_dni, dispatch_uid='update-dni')
