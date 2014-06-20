# -*- encoding: UTF-8 -*-

from core.tests.factories import UserFactory
from cvn import settings as stCVN
from cvn.models import CVN
from decimal import Decimal
from django.test import TestCase
from statistics.models import Department, ProfessionalCategory
import datetime


class CVNTestCase(TestCase):

    @staticmethod
    def _get_member_list(codes):
        member_list = []
        for i in codes:
            member_list.append({'cod_cce': str(i % 2), 'cod_persona': i})
        return member_list

    def _check_dept(self, dept, total, computable, valid):
        # miembros 0-9
        exp_members = Decimal(total)
        # miembros computables => 1, 3, 5, 7, 9
        exp_computable = Decimal(computable)
        # miembros computables con cvn => 3, 9
        exp_valid = Decimal(valid)
        self.assertEqual(dept.number_valid_cvn, exp_valid)
        self.assertEqual(dept.total_members, exp_members)
        self.assertEqual(dept.computable_members, exp_computable)
        self.assertEqual(abs(dept.percentage - exp_valid * 100
                         / exp_computable) <= 0.1, True)

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
        self._check_dept(Department.objects.get(code='1'), 10, 5, 2)
        self._check_dept(Department.objects.get(code='2'), 10, 5, 1)
