# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import CVN
from django.test import TestCase
from core.tests.factories import UserFactory
from statistics.models import Department, ProfessionalCategory
import datetime


class CVNTestCase(TestCase):

    @staticmethod
    def _get_member_list(codes):
        member_list = []
        for i in codes:
            member_list.append({'cod_cce': str(i % 2), 'cod_persona': i})
        return member_list

    def test_calc_statistics(self):
        stats = [
            {
                'departamento': {
                    'nombre': 'Departamento1',
                    'cod_departamento': '1'
                },
                'miembros': self._get_member_list(range(10))
            },
            {
                'departamento': {
                    'nombre': 'Departamento2',
                    'cod_departamento': '2'
                },
                'miembros': self._get_member_list(range(10, 20))
            }
        ]
        ProfessionalCategory.objects.create(**{'code': '0', 'name': 'cat0',
                                               'is_cvn_required': False})
        ProfessionalCategory.objects.create(**{'code': '1', 'name': 'cat1',
                                               'is_cvn_required': True})
        for i in range(20):
            user = UserFactory.create()
            user.profile.rrhh_code = i
            user.profile.documento = i
            user.profile.save()
            cvn = CVN(user_profile=user.profile,
                      status=stCVN.CVNStatus.UPDATED,
                      fecha=datetime.date(1984, 2, 1))
            if i % 3 == 0:
                cvn.status = stCVN.CVNStatus.UPDATED
            elif i % 3 == 1:
                cvn.status = stCVN.CVNStatus.EXPIRED
            else:
                cvn.status = stCVN.CVNStatus.INVALID_IDENTITY
            cvn.save()
        Department.objects.create_all(stats)
        dept = Department.objects.get(code='1')
        #self.assertEqual(dept.number_valid_cvn, 4)
        #self.assertEqual(dept.total)
        # 4 / 10
