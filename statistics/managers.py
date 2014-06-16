# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import UserProfile
from statistics.settings import PROFESSIONAL_CATEGORY
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class DepartmentManager(models.Manager):

    def _create(self, name, code, members):
        data_dept = {}
        data_dept['name'] = name
        data_dept['code'] = code
        num_cvn_update = 0
        num_computable_members = 0
        for member in members:
            try:
                user = UserProfile.objects.get(rrhh_code=member['cod_persona'])
                if (member['cod_cce'] in PROFESSIONAL_CATEGORY):
                    num_computable_members += 1
                    status = user.cvn.status
                    if (status == stCVN.CVNStatus.UPDATED or
                            status == stCVN.CVNStatus.INVALID_IDENTITY):
                        num_cvn_update += 1
            except ObjectDoesNotExist:
                pass
        data_dept['total_members'] = len(members)
        data_dept['computable_members'] = num_computable_members
        data_dept['number_valid_cvn'] = num_cvn_update
        try:
            data_dept['percentage'] = ((num_cvn_update * 100.0) /
                                       num_computable_members)
        except ZeroDivisionError:  # Departments with zero computable members
            data_dept['percentage'] = 100
        return self.model(**data_dept)

    def create_all(self, department_list):
        departments = []
        for department in department_list:
            departments.append(self._create(
                               department['departamento']['nombre'],
                               department['departamento']['cod_departamento'],
                               department['miembros']))
        return super(DepartmentManager, self).bulk_create(departments)
