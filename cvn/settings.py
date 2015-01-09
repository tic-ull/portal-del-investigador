# -*- encoding: UTF-8 -*-

from datetime import date
from django.conf import settings as st
from enum import IntEnum, Enum

import datetime
import os

# Enable translations in this file
_ = lambda s: s

# Default Entity
UNIVERSITY = _(u'Universidad de La Laguna')

# Expiry date for a CVN
EXPIRY_DATE = datetime.date(2013, 12, 31)

# ******************************* PATHS *************************************
REPORTS_PDF_ROOT = os.path.join(st.MEDIA_ROOT, 'cvn/reports/pdf')
REPORTS_CSV_ROOT = os.path.join(st.MEDIA_ROOT, 'cvn/reports/csv')
REPORTS_IMAGES = os.path.join(st.STATIC_ROOT, 'images/')
FILE_TEST_ROOT = os.path.join(st.BASE_DIR, 'cvn/tests/files/')
MIGRATION_ROOT = os.path.join(st.BASE_DIR, 'importCVN')
XML_TEMPLATE = os.path.join(st.BASE_DIR, 'cvn/templates/cvn/xml')
# ******************************* PATHS *************************************

# ******************************* XML FILES *********************************
XML_SKELETON_PATH = os.path.join(XML_TEMPLATE, 'skeleton.xml')
XML_CURRENT_PROFESSION = os.path.join(XML_TEMPLATE, 'current_profession.xml')
XML_PROFESSION = os.path.join(XML_TEMPLATE, 'profession.xml')
XML_TEACHING = os.path.join(XML_TEMPLATE, 'teaching.xml')
XML_LEARNING = os.path.join(XML_TEMPLATE, 'learning.xml')
XML_LEARNING_PHD = os.path.join(XML_TEMPLATE, 'learning_phd.xml')
# ******************************* XML FILES *********************************

# ******************************* URLS **************************************
EDITOR_FECYT = 'https://cvn.fecyt.es/editor/'
# ******************************* URLS **************************************


# ******************************* CVN STATUS ********************************
class CVNStatus(IntEnum):
    UPDATED = 0
    EXPIRED = 1
    INVALID_IDENTITY = 2

CVN_STATUS = (
    (CVNStatus.UPDATED.value, _(u'Actualizado')),
    (CVNStatus.EXPIRED.value, _(u'Caducado')),
    (CVNStatus.INVALID_IDENTITY.value, _(u'NIF/NIE Incorrecto')),
)
# ******************************* CVN STATUS ********************************

# ******************************* CVN WAITING *******************************
# Messages of waiting when be upload a new CVN
MESSAGES_WAITING = {
    0: _(u'Este proceso puede tardar unos minutos, por favor espere.'),
    1: _(u'Se ha establecido la conexión con la FECYT.'
         u' Su CVN se está procesando, por favor espere.'),
    2: _(u'Verificando la información de su CVN, por favor espere.'),
    3: _(u'Este proceso esta tardando más tiempo de lo habitual, por favor espere.'
         u' Si se produce un error repita el proceso.'
         u' Si el error persiste contacte con el %s (%s).' % (st.SUPPORT, st.EMAIL_SUPPORT)),
}

TIME_WAITING = 5000  # In milliseconds
# ******************************* CVN WAITING ********************************

# ******************************* WS FECYT **********************************
FECYT_USER = '<user>'
FECYT_PASSWORD = '<password>'
WS_FECYT_PDF2XML = "https://www.cvnet.es/cvn2RootBean_v1_3/services/Cvn2RootBean?wsdl"
WS_FECYT_XML2PDF = "https://www.cvnet.es/generadorPdfWS_v1_3/services/GenerarPDFWS?wsdl"
WS_FECYT_VERSION = "1.3.0"
FECYT_CVN_NAME = 'CVN'
FECYT_TIPO_PLANTILLA = 'PN2008'
CVN_XML_DATE_FORMAT = '%Y-%m-%d'
# ******************************* WS FECYT **********************************

# ******************************* FECYT ERRORS ******************************
ERROR_CODES = {
    1: _(u'Error general no determinado en el servidor de la FECYT.'),
    2: _(u'El PDF no tiene XML asociado.'),
    3: _(u'El usuario con el que se pretende hacer la importación no existe '
         u'en la base de datos de la FECYT.'),
    4: _(u'Contraseña incorrecta.'),
    5: _(u'El Servicio Web no puede conectarse a la base de datos de '
         u'instituciones de la FECYT.'),
    6: _(u'Error no determinado durante el proceso de autentificación '
         u'con la FECYT.'),
    8: _(u'No se permite realizar importaciones para esta institución.'),
    10: _(u'El CvnRootBean obtenido del XML o del PDF no es válido.'),
    13: _(u'El CVN-XML no es válido.'),
    14: _(u'Fallo en la extracción del CvnRootBean desde el XML.'),
    16: _(u'El XML está vacío.'),
    17: _(u'El proceso de conversión de CvnRootBean de 1.2.5 a 1.3.0 ha '
          u'fallado.')
}
# ******************************* FECYT ERRORS ******************************

# ******************************* FECYT RETURN CODE *************************
RETURN_CODE = {
    '00': _(u'CVN-PDF generado correctamente.'),
    '01': _(u'No se ha podido generar el CVN-PDF.')
}
# ******************************* FECYT RETURN CODE *************************

# ******************************* CVN ITEMS *********************************


class CvnItemCode(Enum):
    # Professional activity
    PROFESSION_CURRENT = '010.010.000.000'
    PROFESSION_FORMER = '010.020.000.000'
    # Learning activity
    LEARNING_DEGREE = '020.010.010.000'
    LEARNING_PHD = '020.010.020.000'
    LEARNING_OTHER = '020.050.000.000'
    # Teaching activity
    TEACHING_SUBJECT = '030.010.000.000'
    TEACHING_PHD = '030.040.000.000'                # Model TesisDoctoral
    # Scientific experience
    SCIENTIFICEXP_PROJECT = '050.020.010.000'       # Model Proyecto
    SCIENTIFICEXP_AGREEMENT = '050.020.020.000'     # Model Convenio
    SCIENTIFICEXP_PROPERTY = '050.030.010.000'      # Model Patente
    # Scientific activity
    SCIENTIFICACT_PRODUCTION = '060.010.010.000'    # Model Publicacion
    SCIENTIFICACT_CONGRESS = '060.010.020.000'      # Model Congreso

# CvnItem > CvnItemID > CVNPF > Item
CVNITEM_CODE = {
    # Actividad científica y tecnológica
    u"060.010.010.000": u'Publicacion',
    u"060.010.020.000": u'Congreso',
    # Experiencia científica y tecnológica
    u"050.020.010.000": u'Proyecto',
    u"050.020.020.000": u'Convenio',
    u"050.030.010.000": u'Patente',
    # Actividad docente
    u"030.040.000.000": u'TesisDoctoral',
}

# CvnItem > Subtype > SubType1 > Item
CVNITEM_SUBTYPE_CODE = {
    u'035': u'Articulo',
    u'148': u'Capitulo',
    u'112': u'Libro',
    u'100': u'TesisDoctoral',
}

REGULAR_DATE_CODE = '040'


# Agent > Identificacion > Personal Identification > OfficialId
class OfficialId(Enum):
    DNI = '000.010.000.100'
    NIE = '000.010.000.110'

# ExternalPK > Type > Item
PRODUCTION_ID_CODE = {
    'FINANCIADORA': '000',
    'ISSN': '010',
    'ISBN': '020',
    'DEPOSITO_LEGAL': '030',
    'SOLICITUD': '060',
}

# Place > CountryCode > Item
PRIORITY_COUNTRY = "050.030.010.120"
EXTENDED_COUNTRY = "050.030.010.220"


# Entity > EntityName code
class Entity(Enum):
    CURRENT_EMPLOYER = "010.010.000.020"
    CURRENT_CENTRE = "010.010.000.060"
    CURRENT_DEPT = "010.010.000.080"
    EMPLOYER = "010.020.000.020"
    CENTRE = "010.020.000.060"
    DEPT = "010.020.000.080"
    UNIVERSITY = "030.010.000.080"
    TEACHING_DEPARTAMENT = "030.010.000.130"
    FACULTY = "030.010.000.540"
    PHD_UNIVERSITY = "030.040.000.080"
    OPERATOR = "050.030.010.250"
    OWNER = "050.030.010.300"


OFFICIAL_TITLE_TYPE = {
    u"DOCTOR": u'940',
    u"LICENCIADO/INGENIERO SUPERIOR": u'950',
    u"DIPLOMADO/INGENIERO TECNICO": u'960'
}

# Indicates 'Link' node contains Congreso data
DATA_CONGRESO = u"110"

# FECYT codes for economic information
ECONOMIC_DIMENSION = {
    # Proyectos
    u"050.020.010.290": u'cuantia_total',
    u"050.020.010.300": u'cuantia_subproyecto',
    u"050.020.010.310": u'porcentaje_en_subvencion',
    u"050.020.010.320": u'porcentaje_en_credito',
    u"050.020.010.330": u'porcentaje_mixto',
    # Convenios
    u"050.020.020.200": u'cuantia_total',
    u"050.020.020.210": u'cuantia_subproyecto',
    u"050.020.020.220": u'porcentaje_en_subvencion',
    u"050.020.020.230": u'porcentaje_en_credito',
    u"050.020.020.240": u'porcentaje_mixto',
}

# Scope for Congresos, Proyectos, Convenios
SCOPE = {
    u"000": u"Autonómica",
    u"010": u"Nacional",
    u"020": u"Unión Europea",
    u"030": u"Internacional no UE",
    u"OTHERS": u"Otros",
}


class ProfessionCode(Enum):
    CURRENT = '010'
    OLD = '020'
    CURRENT_TRIMMED = '10'
    OLD_TRIMMED = '20'


class DedicationType(Enum):
    TOTAL = '020'
    PARTIAL = '030'


class FilterCode(Enum):
    PROGRAM = "030.010.000.140"
    SUBJECT = "030.010.000.190"

PROGRAM_TYPE = {
    u"ARQUITECTO": u"020",
    u"ARQUITECTO TÉCNICO": u"030",
    u"DIPLOMADO/MAESTRO": u"240",
    u"DOCTORADO": u"250",
    u"INGENIERO": u"420",
    u"INGENIERO TÉCNICO": u"430",
    u"LICENCIADO": u"470",
    u"MÁSTER OFICIAL": u"480",
}
PROGRAM_TYPE_OTHERS = "030.010.000.150"

SUBJECT_TYPE = {
    u"TRONCAL": u"000",
    u"OBLIGATORIA": u"010",
    u"OPTATIVA": u"020",
    u"LIBRE CONFIGURACION": u"030",
    u"DOCTORADO": u"050",
}
SUBJECT_TYPE_OTHERS = "030.010.000.430"

# ******************************* CVN ITEMS *********************************

RANGE_OF_YEARS = (1950, date.today().year + 1)  # Range of years for CVN Export

# Unauthorized CVN Authors
CVN_PDF_AUTHOR_NOAUT = [u'FECYT - Author of Example', ]

# ************************* SETTINGS LOCAL ***********************************
try:
    CVN_SETTINGS_LOCAL
except NameError:
    try:
        from .settings_local import *
    except ImportError:
        pass
# ************************* SETTINGS LOCAL ***********************************
