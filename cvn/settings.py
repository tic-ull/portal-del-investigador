# -*- encoding: UTF-8 -*-

from django.conf import settings as st
from enum import IntEnum, Enum
import datetime
import os

# Enable translations in this file
_ = lambda s: s

# FECYT webservice configuration
USER_FECYT = "cvnPdfULL01"
PASSWORD_FECYT = "MXz8T9Py7Xhr"
WS_FECYT_PDF2XML = "https://www.cvnet.es/cvn2RootBean_v1_3/services/Cvn2RootBean?wsdl"
WS_FECYT_XML2PDF = "https://www.cvnet.es/generadorPdfWS_v1_3/services/GenerarPDFWS?wsdl"

# Paths
PDF_ROOT = "cvn/pdf"
XML_ROOT = "cvn/xml"
OLD_PDF_ROOT = os.path.join(st.MEDIA_ROOT, "cvn/old_cvn/")  # CVN antiguos
PDF_DEPT_ROOT = os.path.join(st.MEDIA_ROOT, 'cvn/reports/pdf')
CSV_DEPT_ROOT = os.path.join(st.MEDIA_ROOT, 'cvn/reports/csv')
PDF_DEPT_IMAGES = os.path.join(st.STATIC_ROOT, 'images/')
TEST_ROOT = os.path.join(st.BASE_DIR, 'cvn/tests/files/')


# XML Files for XML parser (to create or modify cvn-xml)

# Base xml-cvn
XML_SKELETON_PATH = os.path.join(st.RES_ROOT, 'cvn/xml/skeleton.xml')

# CVN Items
XML_PROFESSION = os.path.join(st.RES_ROOT, 'cvn/xml/profession.xml')
XML_CURRENT_PROFESSION = os.path.join(st.RES_ROOT, 'cvn/xml/current_profession.xml')
XML_TEACHING = os.path.join(st.RES_ROOT, 'cvn/xml/teaching.xml')
XML_TEACHING_PHD = os.path.join(st.RES_ROOT, 'cvn/xml/doctor.xml')
XML_BACHELOR_ENGINEERING = os.path.join(st.RES_ROOT, 'cvn/xml/bachelor_engineering.xml')
XML_LEARNING_OTHER = os.path.join(st.RES_ROOT, 'cvn/xml/learning_other.xml')

# Optional fragments
XML_2ND_SURNAME = os.path.join(st.RES_ROOT, 'cvn/xml/second_family_name.xml')
XML_OTHERS_TITLE = os.path.join(st.RES_ROOT, 'cvn/xml/others.xml')


# URLs
URL_PDF = os.path.join(st.MEDIA_URL, PDF_ROOT)
URL_XML = os.path.join(st.MEDIA_URL, XML_ROOT)
URL_OLD_CVN = os.path.join(st.MEDIA_URL, OLD_PDF_ROOT)  # CVN antiguos
EDITOR_FECYT = 'https://cvn.fecyt.es/editor/'

# content-type for pdfs
PDF = "application/pdf"

# Log configuration
# XML fetching from FECYT
FILE_LOG_IMPORT = os.path.join(st.PROJECT_ROOT, 'errorCVN.log')
# CVN inserted in database app
FILE_LOG_INSERTADOS = os.path.join(st.PROJECT_ROOT, 'cvnInsertados.log')
# Duplicated CVN
FILE_LOG_DUPLICADOS = os.path.join(st.PROJECT_ROOT, 'cvnDuplicados.log')

# Production unique identifier type
PRODUCCION_ID_CODE = {
    'FINANCIADORA': '000',
    'ISSN': '010',
    'ISBN': '020',
    'DEPOSITO_LEGAL': '030',
    'SOLICITUD': '060',
}
# Production subtype code in xml fecyt branch Subtype/SubType1/Item
FECYT_CODE_SUBTYPE = {
    u'035': u'Articulo',
    u'148': u'Capitulo',
    u'112': u'Libro',
    u'100': u'TesisDoctoral',
}

class FC_OFFICIAL_ID(Enum):
    DNI = '000.010.000.100'
    NIE = '000.010.000.110'

FC_PRIORITY_COUNTRY = "050.030.010.120"
FC_EXTENDED_COUNTRY = "050.030.010.220"
FC_ENTITY_OWNER = "050.030.010.300"
FC_ENITITY_OPERATOR = "050.030.010.250"

class FC_SURNAME(Enum):
    APELLIDO = "000.010.000.010"
    DOCTORANDO = "030.040.000.120"


class FC_OFFICIAL_TITLE_TYPE(Enum):
    T_DOC = '940'
    T_SUP = '950'
    T_MED = '960'
    OTHER = 'OTHER'

class FC_PROFESSION_CODE(Enum):
    CURRENT = '010'
    OLD = '020'


# Indicates 'Link' node contains Congreso data
DATA_CONGRESO = u"110"

# Code of production -- database name of production
FECYT_CODE = {
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

# FECYT codes for economic information of Proyecto
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

# Expiration date for cvn
FECHA_CADUCIDAD = datetime.date(2013, 12, 31)

# FECYT error codes and description
ERROR_CODES = {
    1: _(u'Error general no determinado en el servidor de la FECYT.'),
    2: _(u'El PDF no tiene XML asociado.'),
    3: _(u'El usuario con el que se pretende hacer la importación no existe '
         'en la base de datos de la FECYT.'),
    4: _(u'Contraseña incorrecta.'),
    5: _(u'El Servicio Web no puede conectarse a la base de datos de '
         'instituciones de la FECYT.'),
    6: _(u'Error no determinado durante el proceso de autentificación '
         'con la FECYT.'),
    8: _(u'No se permite realizar importaciones para esta institución.'),
    10: _(u'El CvnRootBean obtenido del XML o del PDF no es válido.'),
    13: _(u'El CVN-XML no es válido.'),
    14: _(u'Fallo en la extracción del CvnRootBean desde el XML.'),
    16: _(u'El XML está vacío.'),
    17: _(u'El proceso de conversión de CvnRootBean de 1.2.5 a 1.3.0 ha '
          'fallado.')
}

REGULAR_DATE_CODE = '040'


class CVNStatus(IntEnum):
    UPDATED = 0
    EXPIRED = 1
    INVALID_IDENTITY = 2

CVN_STATUS = (
    (CVNStatus.UPDATED.value, _(u'Actualizado')),
    (CVNStatus.EXPIRED.value, _(u'Caducado')),
    (CVNStatus.INVALID_IDENTITY.value, _(u'NIF/NIE Incorrecto')),
)

# Messages for waiting when be upload a new CVN
MESSAGES_WAITING = {
    0: _(u'Este proceso puede tardar unos minutos, por favor espere.'),
    1: _(u'Se ha establecido la conexión con la FECYT.'
         u' Su CVN se está procesando, por favor espere.'),
    2: _(u'Verificando la información de su CVN, por favor espere.'),
    3: _(u'Este proceso esta tardando más tiempo de lo habitual, por favor espere.'
         u' Si se produce un error repita el proceso.'
         u' Si el error persiste contacte con el Servicio de Investigación (sopinve@ull.es).'),
}

# In milliseconds
TIME_WAITING = 5000
