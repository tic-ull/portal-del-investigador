# -*- encoding: UTF-8 -*-

import os
from django.conf import settings as st

# Usuario Administrador de la plantilla de administración de Django
ADMIN_USERNAME = "admin"

# Datos para la comunicación con el Web Service del FECYT
USER_WS = "cvnPdfULL01"
PASSWD_WS = "MXz8T9Py7Xhr"
URL_WS = "https://www.cvnet.es/cvn2RootBean_v1_3/services/Cvn2RootBean?wsdl"

# Rutas de los XML y PDF
PDF_ROOT = "cvn/pdf"
XML_ROOT = "cvn/xml"
OLD_PDF_ROOT = "cvn/old_cvn/"  # CVN antiguos
PDF_DEPT_ROOT = os.path.join(st.MEDIA_ROOT, 'cvn/pdf_departamento')
PDF_DEPT_IMAGES = os.path.join(st.STATIC_ROOT, 'images/')

URL_PDF = os.path.join(st.MEDIA_URL, PDF_ROOT)
URL_XML = os.path.join(st.MEDIA_URL, XML_ROOT)
URL_OLD_CVN = os.path.join(st.MEDIA_URL, OLD_PDF_ROOT)  # CVN antiguos

# Tipo de ficheros de subida
PDF = "application/pdf"

# Ficheros con los resultados de las diferentes operaciones
# Fichero con los errores al obtener el XML utilizando el WS del FECYT
FILE_LOG_IMPORT = os.path.join(st.PROJECT_ROOT, 'errorCVN.log')
# Fichero con los CVN con datos insertados en la BBDD de la aplicación
FILE_LOG_INSERTADOS = os.path.join(st.PROJECT_ROOT, 'cvnInsertados.log')
# Fichero que almacena los CVN duplicados.
FILE_LOG_DUPLICADOS = os.path.join(st.PROJECT_ROOT, 'cvnDuplicados.log')

# Equivalencias entre los tags de los nodos XML y los campos de la BBDD
DIC_PERSONAL_DATA_XML = {
    u'GivenName': u'nombre',
    u'FirstFamilyName': u'primer_apellido',
    u'SecondFamilyName': u'segundo_apellido',
    u'Nacionality': u'nacionalidad',
    u'BirthDate': u'fecha_nacimiento',
    u'BirthCountry': u'pais_de_nacimiento',
    u'BirthRegion': u'comunidad_nacimiento',
    u'BirthCity': u'ciudad_de_nacimiento',
    u'Gender': u'sexo',
    u'City': u'ciudad_de_contacto',
    u'Streets': u'direccion',
    u'OtherInformation': u'resto_direccion',
    u'PostalCode': u'codigo_postal',
    u'Region':  u'comunidad',
    u'CountryCode': u'pais_de_contacto',
    u'Province': u'provincia',
    u'Telephone': u'telefono_',
    u'Fax': u'telefono_fax_',
    u'PersonalWeb': u'pagina_web_personal',
    u'InternetEmailAddress': u'correo_electronico',
    u'Photo': u'imagen',
}

# Editor FECYT (Paso 6): Actividad Científica y tecnológica
ACTIVIDAD_CIENTIFICA_TIPO_PUBLICACION = {
    u'035': u'Articulo',
    u'148': u'Capitulo de Libro',
    u'112': u'Libro',
}

# Indica que el nodo 'Link' contiene los datos del congreso
DATA_CONGRESO = u"110"
# Indica que el nodo 'Link' contiene los datos de una tesis
DATA_TESIS = u"100"

# Devuelve las tabla correspondiente donde almacenar los datos
MODEL_TABLE = {
    # Actividad científica y tecnológica
    u"060.010.010.000": u'Publicacion',
    u"060.010.020.000": u'Congreso',
    # Experiencia científica y tecnológica
    u"050.020.010.000": u'Proyecto',
    u"050.020.020.000": u'Convenio',
    # Actividad docente
    u"030.040.000.000": u'TesisDoctoral',
}

# Diccionario para las cuantías de las financiaciones
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

# Ámbito de Congresos, Proyectos y Convenios
SCOPE = {
    u"000": u"Autonómica",
    u"010": u"Nacional",
    u"020": u"Unión Europea",
    u"030": u"Internacional no UE",
    u"OTHERS": u"Otros",
}

# Fecha de caducidad de un CVN
CVN_CADUCIDAD = 1   # Año

# Dato de la página introducido en un formato no reconocible
INVALID_PAGE = -1
# Indica que no se ha podido crear un diccionario de búsqueda
INVALID_SEARCH = -1

# Errores FECYT
ERROR_CODES = {
    1: u'Error en el servidor',
    2: u'El PDF no tenía XML incrustado',
    3: u'El usuario con el que se pretende hacer la importación no existe\
         en la base de datos',
    4: u'Contraseña incorrecta',
    5: u'La base de datos de instituciones no está accesible para el\
         servicio web',
    6: u'Error no determinado en el procesdo de autentificación',
    8: u'No se permiten importaciones para esta institución',
    10: u'El CvnRootBean obtenido del XML o PDF no es válido',
    13: u'El CVN-XML no es válido',
    14: u'No se ha podido extraer el CVNRootBean desde el CVN-XML',
    16: u'El XML viene vacío',
    17: u'El proceso de conversión de CVNRootBean de 1.2.5 a 1.3.0\
          ha fallado'
}
