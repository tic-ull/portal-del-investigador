# -*- encondig: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import Articulo, Capitulo, Libro
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from lxml import etree
from parser_helpers import parse_nif


def scientific_production_to_context(user_profile, context):
    try:
        user_profile.cvn
        context['Articulos'] = Articulo.objects.filter(
            user_profile=user_profile)
        context['Capitulos'] = Capitulo.objects.filter(
            user_profile=user_profile)
        context['Libros'] = Libro.objects.filter(
            user_profile=user_profile)
        context['Congresos'] = user_profile.congreso_set.all()
        context['Proyectos'] = user_profile.proyecto_set.all()
        context['Convenios'] = user_profile.convenio_set.all()
        context['TesisDoctorales'] = user_profile.tesisdoctoral_set.all()
        return True
    except ObjectDoesNotExist:
        return False


def cvn_to_context(user, context):
    try:
        context['cvn'] = user.cvn
        context['cvn_status'] = stCVN.CVN_STATUS[user.cvn.status][1]
        if user.cvn.status == stCVN.CVNStatus.INVALID_IDENTITY:
            if user.cvn.xml_file.closed:
                user.cvn.xml_file.open()
            xml_tree = etree.parse(user.cvn.xml_file)
            user.cvn.xml_file.seek(0)
            nif = parse_nif(xml_tree)
            user.cvn.xml_file.close()
            if nif is not '':
                context['nif_invalid'] = nif.upper()
            else:
                context['nif_invalid'] = _(u'Desconocido')
    except ObjectDoesNotExist:
        return


def isdigit(obj):
    if type(obj) is str and obj.isdigit():
        return True
    else:
        return False


def noneToZero(value):
    return value if value is not None else 0
