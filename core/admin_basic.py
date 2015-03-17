# -*- encoding: UTF-8 -*-

#
#    Copyright 2015
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

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _


class BasicAdminSite(AdminSite):
    site_header = _(u'Administración Básica')

    def has_permission(self, request):
        return request.user.has_perm('auth.basic_staff')

basic_admin_site = BasicAdminSite(name='basic_admin')
basic_admin_site.login = login_required(basic_admin_site.login)
