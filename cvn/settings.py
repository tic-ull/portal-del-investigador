# -*- encoding: utf-8 -*-
# Modelos BBDD
from cvn.models import *

import os
from django.conf import settings as st

# Usuario Administrador de la plantilla de administración de Django
ADMIN_USERNAME = "admin"

# Datos para la comunicación con el Web Service del Fecyt
USER_WS = "cvnPdfULL01"
PASSWD_WS = "MXz8T9Py7Xhr"
URL_WS = "https://www.cvnet.es/cvn2RootBean_v1_3/services/Cvn2RootBean?wsdl"

# Rutas de los XML y PDF
URL_BASE = os.path.join(st.MEDIA_ROOT, 'cvn')  # TODO: Poner la ruta de viinv donde están los pdfs y xmls
URL_PDF = os.path.join(URL_BASE, "pdf/")
URL_XML = os.path.join(URL_BASE, "xml/")
URL_OLD_CVN = os.path.join(URL_BASE, "old_cvn/")  # CVN antiguos
RUTA_BBDD = os.path.join(st.MEDIA_ROOT, 'files/cvn/')

# Tipo de ficheros de subida
PDF = "application/pdf"

# Ruta de los PDFs para servirlo desde la app
MEDIA_PDF = os.path.join(st.MEDIA_URL, 'cvn/pdf/')

# Ficheros con los resultados de las diferentes operaciones
FILE_LOG_IMPORT =  os.path.join(st.PROJECT_ROOT, 'errorCVN.log')          # Fichero con los errores al obtener el XML utilizando el WS del Fecyt
FILE_LOG_INSERTADOS = os.path.join(st.PROJECT_ROOT, 'cvnInsertados.log') # Fichero con los CVN cuyos datos han sido insertados en la BBDD de la aplicación
FILE_LOG_DUPLICADOS = os.path.join(st.PROJECT_ROOT, 'cvnDuplicados.log') # Fichero que almacena los CVN duplicados.

# Almacena las equivalencias entre los tags de los nodos XML y los campos de la BBDD
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

# Editor Fecyt (Paso 6): Actividad Científica y tecnológica
ACTIVIDAD_CIENTIFICA_TIPO_PUBLICACION = {
u'035': u'Artículo',
u'148': u'Capítulo de Libro',
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
CVN_CADUCIDAD = 1 # Año

# Constante para indicar que el dato de la página está introducido en un formato no reconocible
INVALID_PAGE = -1
# Constante para indicar que no se ha podido crear un diccionario de búsqueda
INVALID_SEARCH = -1
