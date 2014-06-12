# -*- encoding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cvn import settings as stCVN
from cvn.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
# PROFESSIONAL CATEGORY TABLE
from statistics.settings import PROFESSIONAL_CATEGORY


class Department(models.Model):
    name = models.CharField(_('Nombre'), max_length=40, unique=True)
    code = mdoels.CharField(_(u'Código departamento'), max_length=10)
    number_valid_cvn = models.IntegerField(_(u'Número de CVN válidos'))
    computable_members = models.IntegerField(_(u'Miembros computables'))
    total_member = models.IntegerField(_('Miembros totales'))
    percentage = models.DecimalField(_(u'Porcentaje de CVN válidos'),
                                     max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.name

    @staticmethod
    def calculate_statistics(department_name, member_list, code):
        num_valid_cvn = 0
        num_computable_members = 0
        for member in members_list:
            try:
                user = UserProfile.objects.get(rrhh_code=member['cod_persona'])
                if (member['cod_cce'] in PROFESSIONAL_CATEGORY):
                    num_computable_members += 1
                    if (user.cvn.status == stCVN.CVNStatus.UPDATED or
                            user.cvn.status == stCVN.CVNStatus.INVALID_IDENTITY):
                        num_valid_cvn += 1
            except ObjectDoesNotExist:
                pass
        self.name = department_name
        self.code = code
        self.total_member = len(member_list)
        self.computable_members = num_computable_members
        self.number_valid_cvn = num_valid_cvn
        try:
            self.percentage = ((num_valid_cvn * 100.0) /
                               num_computable_members)
        except ZeroDivisionError:  # Departments with zero computable members
            self.percentage = 100
        self.save()
