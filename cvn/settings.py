# -*- encoding: utf-8 -*-
# Modelos BBDD
from cvn.models import *

import os

# Datos para la comunicación con el Web Service del Fecyt
USER_WS = "cvnPdfULL01"
PASSWD_WS = "MXz8T9Py7Xhr"
URL_WS = "https://www.cvnet.es/cvn2RootBean_v1_3/services/Cvn2RootBean?wsdl"

# Rutas de los XML y PDF
URL_BASE = "/../static/files/"
URL_PDF = os.getcwd() + URL_BASE + "pdf/"
URL_XML = os.getcwd() + URL_BASE + "xml/"

# Ficheros con los resultados de las diferentes operaciones
FILE_LOG_IMPORT = "../static/files/import/errorCVN.log"       # Fichero con los errores al obtener el XML utilizando el WS del Fecyt
FILE_LOG_ERROR  = "../static/files/import/errorImport.log"    # Fichero con los errores al importar a la BBDD de la app CVN.
FILE_LOG_DUPLICADOS = "../static/files/import/cvnDuplicados.log" # Fichero que almacena los CVN duplicados.

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
u"060.010.010.000": Publicacion,
u"060.010.020.000": Congreso,
# Experiencia científica y tecnológica
u"050.020.010.000": Proyecto,
u"050.020.020.000": Convenio,
# Actividad docente
u"030.040.000.000": TesisDoctoral,
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

# Constante para indicar que el dato de la página está introducido en un formato no reconocible
INVALID_PAGE = -1
# Constante para indicar que no se ha podido crear un diccionario de búsqueda
INVALID_SEARCH = -1
