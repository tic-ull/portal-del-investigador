# -*- encoding: UTF-8 -*-

from django.conf import settings as st
from enum import Enum
import datetime
import os

# Enable translations in this file
_ = lambda s: s

# FECYT webservice configuration
USER_WS = "cvnPdfULL01"
PASSWD_WS = "MXz8T9Py7Xhr"
URL_WS = "https://www.cvnet.es/cvn2RootBean_v1_3/services/Cvn2RootBean?wsdl"

# Paths
PDF_ROOT = "cvn/pdf"
XML_ROOT = "cvn/xml"
OLD_PDF_ROOT = os.path.join(st.MEDIA_ROOT, "cvn/old_cvn/")  # CVN antiguos
PDF_DEPT_ROOT = os.path.join(st.MEDIA_ROOT, 'cvn/pdf_departamento')
PDF_DEPT_IMAGES = os.path.join(st.STATIC_ROOT, 'images/')
TEST_ROOT = os.path.join(st.BASE_DIR, 'cvn/tests/files/')

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
}
# Production subtype code in xml fecyt branch Subtype/SubType1/Item
FECYT_CODE_SUBTYPE = {
    u'035': u'Articulo',
    u'148': u'Capitulo',
    u'112': u'Libro',
    u'100': u'TesisDoctoral',
}

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


class CVNStatus(Enum):
    UPDATED = 0
    EXPIRED = 1
    INVALID_IDENTITY = 2

CVN_STATUS = (
    (CVNStatus.UPDATED, _(u'Actualizado')),
    (CVNStatus.EXPIRED, _(u'Caducado')),
    (CVNStatus.INVALID_IDENTITY, _(u'NIF/NIE Incorrecto')),
)

# Messages for waiting when be upload a new CVN
MESSAGES_WAITING = {
    1: _(u'Este proceso puede tardar unos minutos, por favor espere.'),
    2: _(u'Se ha establecido la conexión con la FECYT. Su CVN se está procesando, por favor espere.'),
    3: _(u'Verificando la información de su CVN, por favor espere.'),
    4: _(u'Este proceso esta tardando más tiempo de lo habitual, por favor espere.'
         u'Si se produce un error repita el proceso.'
         u'Si el error persiste contacte con el Servicio de Investigación (sopinve@ull.es).')
}
