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
from django.contrib.admin.templatetags.admin_modify import register
from django.contrib.admin.templatetags.admin_modify import submit_row as osr


# If the developer wants to enable/disable the save buttons,
# we want to give preference over Django's logic
# https://github.com/django/django/blob/master/django/contrib/admin/templatetags/admin_modify.py#L23
@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = osr(context)  # Here is Django's logic => it ignores the context
    if 'show_save_and_continue' in context:
        ctx['show_save_and_continue'] = context['show_save_and_continue']
    if 'show_save' in context:
        ctx['show_save'] = context['show_save']
    return ctx

import admin_advanced  # Don't delete
import admin_basic  # Don't delete
