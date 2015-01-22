# -*- encoding: UTF-8 -*-

#
#    Copyright 2014-2015 STIC-Investigación - Universidad de La Laguna (ULL)
#    <gesinv@ull.edu.es>
#
#    This file is part of Portal del Investigador.
#
#    Portal del Investigador is free software: you can redistribute it and/or
#    modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Portal del Investigador is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Portal del Investigador.  If not, see
#    <http://www.gnu.org/licenses/>.
#

from django import forms
from django.utils.safestring import mark_safe
from string import Template


class FileFieldURLWidget(forms.TextInput):

    def render(self, name, value, attrs=None):
        if value:
            tpl = Template(u"<a href='%s'>%s</a>" % (value.url, value.name))
            return mark_safe(tpl.template)
