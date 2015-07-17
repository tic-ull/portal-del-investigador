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
    attributes = request.session['attributes']

    if attributes['NumDocumento'] != user.profile.documento:
        rrhh_code1 = ws.get(url=(st.WS_COD_PERSONA %
                                 attributes['NumDocumento']), use_redis=False)
        rrhh_code2 = ws.get(url=(st.WS_COD_PERSONA %
                                 user.profile.documento), use_redis=False)
        if rrhh_code1 == rrhh_code2:
            user.profile.change_dni(attributes['NumDocumento'])
            user.save()

user_logged_in.connect(update_user, dispatch_uid='update-profile')
user_logged_in.connect(update_dni, dispatch_uid='update-dni')
