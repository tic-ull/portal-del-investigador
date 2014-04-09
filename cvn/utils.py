# -*- encondig: UTF-8 -*-

from cvn import settings as stCVN
from dateutil.relativedelta import relativedelta
import datetime


def saveScientificProductionToContext(usuario, context):
    context['Publicaciones'] = usuario.publicacion_set.all()
    context['Congresos'] = usuario.congreso_set.all()
    context['Proyectos'] = usuario.proyecto_set.all()
    context['Convenios'] = usuario.convenio_set.all()
    context['TesisDoctorales'] = usuario.tesisdoctoral_set.all()


def getDataCVN(cvn=None):
    context = {}
    context['fecha_cvn'] = cvn.fecha_cvn
    date = relativedelta(years=stCVN.CVN_CADUCIDAD)
    if (cvn.fecha_cvn + date) < datetime.date.today():
        context['updateCVN'] = True
    else:
        context['fecha_valido'] = cvn.fecha_cvn + date
    return context


def isdigit(obj):
    if type(obj) is str and obj.isdigit():
        return True
    else:
        return False


def noneToZero(value):
    return value if not value is None else 0
