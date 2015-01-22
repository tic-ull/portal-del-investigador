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

from django.core.management.base import BaseCommand
from core.models import UserProfile


class Command(BaseCommand):
    help = u'Sync user rrhh code'

    def handle(self, *args, **options):
        try:
            for profile in UserProfile.objects.all():
                profile.update_rrhh_code()
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
