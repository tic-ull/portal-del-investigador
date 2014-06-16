# -*- encoding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from statistics.managers import StatsManager
from core.models import UserProfile
import statistics.settings as stSt
import cvn.settings as stCVN
from django.core.exceptions import ObjectDoesNotExist


class Stats(models.Model):
    name = models.CharField(_('Nombre'), max_length=40, unique=True)
    code = models.CharField(_(u'Código departamento'), max_length=10)
    number_valid_cvn = models.IntegerField(_(u'Número de CVN válidos'))
    computable_members = models.IntegerField(_(u'Miembros computables'))
    total_members = models.IntegerField(_('Miembros totales'))
    percentage = models.DecimalField(_(u'Porcentaje de CVN válidos'),
                                     max_digits=5, decimal_places=2)
    objects = StatsManager()

    def update(self, name, members, commit=False):
        self.name = name
        num_cvn_update = 0
        num_computable_members = 0
        for member in members:
            try:
                if (member['cod_cce'] in stSt.PROFESSIONAL_CATEGORY):
                    num_computable_members += 1
                    user = UserProfile.objects.get(
                        rrhh_code=member['cod_persona'])
                    if user.cvn.status != stCVN.CVNStatus.EXPIRED:
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
        abstract = True


class Department(Stats):
    pass


class Area(Stats):
    pass
