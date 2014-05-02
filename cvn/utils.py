# -*- encondig: UTF-8 -*-

from cvn import settings as stCVN
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
import datetime


def scientific_production_to_context(user, context):
    try:
        user.cvn
        context['Publicaciones'] = user.publicacion_set.all()
        context['Congresos'] = user.congreso_set.all()
        context['Proyectos'] = user.proyecto_set.all()
        context['Convenios'] = user.convenio_set.all()
        context['TesisDoctorales'] = user.tesisdoctoral_set.all()
        return True
    except ObjectDoesNotExist:
        return False


def date_cvn_to_context(user, context):
    try:
        context['fecha_cvn'] = user.cvn.fecha_cvn
        date = relativedelta(years=stCVN.CVN_CADUCIDAD)
        if (user.cvn.fecha_cvn + date) < datetime.date.today():
            context['updateCVN'] = True
        else:
            context['fecha_valido'] = user.cvn.fecha_cvn + date
    except ObjectDoesNotExist:
        return


def isdigit(obj):
    if type(obj) is str and obj.isdigit():
        return True
    else:
        return False


def noneToZero(value):
    return value if not value is None else 0
