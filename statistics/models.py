# -*- encoding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from statistics.managers import DepartmentManager
#from cvn import settings as stCVN
#from cvn.models import UserProfile
#from django.core.exceptions import ObjectDoesNotExist
# PROFESSIONAL CATEGORY TABLE
#from statistics.settings import PROFESSIONAL_CATEGORY


class Department(models.Model):
    name = models.CharField(_('Nombre'), max_length=40, unique=True)
    code = models.CharField(_(u'Código departamento'), max_length=10)
    number_valid_cvn = models.IntegerField(_(u'Número de CVN válidos'))
    computable_members = models.IntegerField(_(u'Miembros computables'))
    total_members = models.IntegerField(_('Miembros totales'))
    percentage = models.DecimalField(_(u'Porcentaje de CVN válidos'),
                                     max_digits=5, decimal_places=2)
    objects = DepartmentManager()

    def __unicode__(self):
        return self.name
