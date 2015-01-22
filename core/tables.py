# -*- encoding: UTF-8 -*-

#
#    Copyright 2014-2015 STIC-Investigación - Universidad de La Laguna (ULL) <gesinv@ull.edu.es>
#
#    This file is part of Portal del Investigador.
#
#    Portal del Investigador is free software: you can redistribute it and/or modify
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
#    along with Portal del Investigador.  If not, see <http://www.gnu.org/licenses/>.
#

import django_tables2 as tables


class Table(tables.Table):

    def __init__(self, *args, **kwargs):
        columns = kwargs.pop('columns', None)
        super(Table, self).__init__(*args, **kwargs)
        if columns is None:
            return
        for i in range(0, len(self.columns.all())):
            try:
                self.columns[i].column.attrs = columns[i]
            except KeyError:
                self.columns[i].column.visible = False
