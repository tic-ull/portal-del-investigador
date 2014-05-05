# -*- encondig: UTF-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from cvn import settings as stCVN


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


def cvn_to_context(user, context):
    try:
        context['cvn'] = user.cvn
        context['cvn_status'] = stCVN.CVN_STATUS[int(user.cvn.status)][1]
    except ObjectDoesNotExist:
        return


def isdigit(obj):
    if type(obj) is str and obj.isdigit():
        return True
    else:
        return False


def noneToZero(value):
    return value if value is not None else 0
