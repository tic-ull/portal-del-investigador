# -*- encondig: UTF-8 -*-

from cvn import settings as stCVN
from dateutil.relativedelta import relativedelta
import datetime


def scientific_production_to_context(user, context):
    if not user.cvn:
        return False
    context['Publicaciones'] = user.publicacion_set.all()
    context['Congresos'] = user.congreso_set.all()
    context['Proyectos'] = user.proyecto_set.all()
    context['Convenios'] = user.convenio_set.all()
    context['TesisDoctorales'] = user.tesisdoctoral_set.all()
    return True


def date_cvn_to_context(cvn, context):
    if not cvn:
        return
    context['fecha_cvn'] = cvn.fecha_cvn
    date = relativedelta(years=stCVN.CVN_CADUCIDAD)
    if (cvn.fecha_cvn + date) < datetime.date.today():
        context['updateCVN'] = True
    else:
        context['fecha_valido'] = cvn.fecha_cvn + date


def isdigit(obj):
    if type(obj) is str and obj.isdigit():
        return True
    else:
        return False


def noneToZero(value):
    return value if not value is None else 0
