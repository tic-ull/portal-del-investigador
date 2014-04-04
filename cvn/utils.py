# -*- encondig: UTF-8 -*-

from cvn import settings as stCVN
from dateutil.relativedelta import relativedelta
from django.conf import settings as st
from django.core.files.move import file_move_safe
import datetime
import os


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


def movOldCVN(cvn):
    if not cvn:
        pass
    cvn_file = os.path.join(st.MEDIA_ROOT, cvn.cvn_file.name)
    old_path = os.path.join(st.MEDIA_ROOT, stCVN.OLD_PDF_ROOT)
    new_file_name = cvn.cvn_file.name.split('/')[-1].replace(
        u'.pdf', u'-' + str(
            cvn.updated_at.strftime('%Y-%m-%d')
        ) + u'.pdf')
    old_cvn_file = os.path.join(old_path, new_file_name)
    if not os.path.isdir(old_path):
        os.makedirs(old_path)
    file_move_safe(cvn_file, old_cvn_file, allow_overwrite=True)


def isdigit(obj):
    if type(obj) is str and obj.isdigit():
        return True
    else:
        return False


def noneToZero(value):
    return value if not value is None else 0
