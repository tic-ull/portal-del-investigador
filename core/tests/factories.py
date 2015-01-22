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

from core.models import UserProfile
from django.contrib.auth.models import User
from random import randint

import factory


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'juan{0}'.format(n))
    first_name = 'Juan'
    last_name = 'Doe'
    email = 'juan@example.com'

    @factory.post_generation
    def create_profile(self, *args, **kwargs):
        NIF = 'TRWAGMYFPDXBNJZSQVHLCKE'
        dni = randint(10000000, 99999999)
        UserProfile.objects.create(
            user=self, documento=str(dni) + NIF[dni % 23])


class AdminFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'admin{0}'.format(n))
    is_superuser = True
    is_staff = True
