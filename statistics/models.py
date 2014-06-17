# -*- encoding: UTF-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _
from statistics.managers import StatsManager
from core.models import UserProfile
import statistics.settings as stSt
import cvn.settings as stCVN
import json
import urllib


class Stats(models.Model):
    name = models.CharField(_(u'Nombre'), max_length=40, unique=True)
    code = models.CharField(_(u'Código departamento'), max_length=10)
    number_valid_cvn = models.IntegerField(_(u'Número de CVN válidos'))
    computable_members = models.IntegerField(_(u'Miembros computables'))
    total_members = models.IntegerField(_(u'Miembros totales'))
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
                    status = user.cvn.status
                    if (status == stCVN.CVNStatus.UPDATED or
                            status == stCVN.CVNStatus.INVALID_IDENTITY):
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


class ProfessionalCategory(models.Model):
    code = models.CharField(_(u'Código de categoría'), max_length=10,
                            unique=True)
    name = models.CharField(_(u'Categoría'), max_length=255)
    is_cvn_required = models.NullBooleanField(_(u'CVN requerido'))

    @staticmethod
    def update(past_days=0):
        categories = json.loads(
            urllib.urlopen(stSt.WS_CATEGORY % past_days).read())
        for category in categories:
            try:
                pc = ProfessionalCategory.objects.get(code=category['id'])
                if pc.name != category['descripcion']:
                    pc.name = category['descripcion']
                    pc.save()
            except ObjectDoesNotExist:
                ProfessionalCategory.objects.create(
                    **{'name': category['descripcion'],
                       'code': category['id']})

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _(u'Professional categories')
