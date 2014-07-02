# -*- encoding: UTF-8 -*-

from core.models import UserProfile
from core.utils import wsget
from cvn import settings as stCVN
from django.conf import settings as st
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _
from statistics.managers import StatsManager, ProfessionalCategoryManager


class Stats(models.Model):
    name = models.CharField(_(u'Nombre'), max_length=40, unique=True)
    code = models.CharField(_(u'Código departamento'), max_length=10)
    number_valid_cvn = models.IntegerField(_(u'CVN válidos'))
    computable_members = models.IntegerField(_(u'Miembros computables'))
    total_members = models.IntegerField(_(u'Miembros totales'))
    percentage = models.DecimalField(_(u'Porcentaje CVN válidos'),
                                     max_digits=5, decimal_places=2)
    objects = StatsManager()

    def update(self, name, members, commit=False):
        self.name = name
        num_cvn_update = 0
        num_computable_members = 0
        for member in members:
            try:
                if ProfessionalCategory.objects.get(
                        code=member['cod_cce']).is_cvn_required is True:
                    num_computable_members += 1
                    user = UserProfile.objects.get(
                        rrhh_code=member['cod_persona'])
                    if user.cvn.status == stCVN.CVNStatus.UPDATED:
                        num_cvn_update += 1
            except ObjectDoesNotExist:
                pass
        self.total_members = len(members)
        self.computable_members = num_computable_members
        self.number_valid_cvn = num_cvn_update
        try:
            self.percentage = num_cvn_update * 100.0 / num_computable_members
        except ZeroDivisionError:  # Departments with zero computable members
            self.percentage = 100
        if commit:
            self.save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        abstract = True


class Department(Stats):

    @staticmethod
    def get_user_department(rrhh_code):
        try:
            dept_json = wsget(st.WS_INFO_USER % rrhh_code)
            dept = Department.objects.get(
                code=dept_json['departamento']['cod_departamento'])
        except (KeyError, ObjectDoesNotExist):
            return None, None
        return dept, dept_json


class Area(Stats):
    pass


class ProfessionalCategory(models.Model):
    code = models.CharField(_(u'Código de categoría'), max_length=10,
                            unique=True)
    name = models.CharField(_(u'Categoría'), max_length=255)
    is_cvn_required = models.NullBooleanField(_(u'CVN requerido'))
    objects = ProfessionalCategoryManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _(u'Professional categories')
