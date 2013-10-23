# -*- encoding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Excepción para la búsqueda de objetos en la BBDD
from django.core.exceptions import ObjectDoesNotExist

# BBDD de Viinv
from viinvDB.models import GrupoinvestInvestigador, GrupoinvestInvestcvn, AuthUser, GrupoinvestCategoriainvestigador
from cvn.models import *
# BBDD de CVN (GI)

# Constantes para la conexión con el Web Service del Fecyt
from cvn.settings import USER_WS, PASSWD_WS, URL_WS

# Conexión con Web Service
import suds   
import binascii
import base64 # Codificación para el web service del Fecyt

# Clase para importar los datos de un XML a la BBDD
from cvn.utilsCVN import UtilidadesXMLtoBBDD

# #########################################################################################################
# TODO: Deberían ir en un fichero de settings para tests
import os
# Settings de la aplicación
from django.conf import settings as setts
# Constantes para los tests
ID_TEST  = 99999
USERNAME = 'testCVN'
PASSWORD = '123'
ATTR     = {'username': 'testCVN', 'first_name': 'Test', 'last_name': 'Testing CVN', 
			'TipoDocumento': 'NIF', 'NumDocumento': '123456789V', 
			'ou': ['PDI', 'srv_wifi', 'Alumnos', 'srv_soft', 'rol_becario', 'srv_webpages', 'srv_ddv', 
					'srv_vpn', 'CCTI', 'srv_siga_ull.es', 'NACFicheros', 'Act', 'srv_google', 'srv_siga'],
					'email': 'test@ull.edu.es'}
TEST_LOGIN_URL = 'http://testserver/investigacion/accounts/login/?next=/investigacion/cvn/download/'
TEST_LOGIN     = 'http://testserver/investigacion/accounts/login/'			
# TODO: Añadir la ruta desde una variable del settings que ya está configurada para ello.			
CVN_FILE = os.path.join(setts.MEDIA_ROOT, 'cvn/pdf/CVN-test-709bddb1.pdf')
XML_FILE = os.path.join(setts.MEDIA_ROOT, 'cvn/xml/CVN-test-709bddb1.xml')
# #########################################################################################################

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class UserAccessTest(TestCase):
	"""
		Tests de funcionalidades del usuario.
	"""
	def setUp(self):
		"""
			Método que se ejecuta antes de cada test de la clase para la configuración inicial de los mismos
		"""		
		self.user = User.objects.create(username=USERNAME, email=ATTR['email'])
		# Se añade la clave con el cifrado utilizado por Django
		self.user.set_password(PASSWORD)
		self.user.save()		
		# Cliente para los test de funcinalidades
		self.client = Client()		
		
				
	#~ def tearDown(self):
		#~ """
			#~ Método que se ejecuta después de cada test de la clase
		#~ """		
		#~ print ">>>> tearDown"
		#~ try:
			#~ GrupoinvestInvestcvn.objects.get(pk=ID_TEST).delete()
			#~ print ">>>> >>>>> tearDown ----> delete()"
			#~ print GrupoinvestInvestcvn.objects.get(pk=ID_TEST)
		#~ except ObjectDoesNotExist:
			#~ pass # No se ha ejecutado el test que crea dicho objeto
		
		
	def test_login(self):
		"""
			Test: Usuario registrado puede acceder a la aplicación.
		"""						
		# El usuario creado se puede loguear.			
		response = self.client.login(username = USERNAME, password = PASSWORD)
		self.assertTrue(response)
		# Sale de la sesión
		self.client.logout()
		

	def test_download_cvn_anonymous(self):		
		"""
			Test: Usuario anónimo accede a la ruta (de forma manual) de descarga 
				del CVN -> redirección a la página de acceso CAS.
			
			Notas:
				302 Found: The requested resource resides temporarily under a different URI.
		"""
		# Un usuario anónimo accede a la ruta de descarga del CVN		
		response = self.client.get(reverse('downloadCVN'))#, follow=True)
		self.assertEqual(response.status_code, 302) # Se redirige hacia la página de acceso CAS
		self.assertEqual(response._headers['location'][1], TEST_LOGIN_URL)


	def test_download_cvn_user_withoutCVN(self):		
		"""
			Test: Usuario registrado que no ha subido CVN, accede a la página de descarga 
				(añadiendo url de forma manual) -> error 404.
				
			Notas: 
				404 Not Found: The server has not found anything matching the Request-URI.
				
			Importante: Se lanza el 404 en el código a través de un "raise http404". Cambiar si es necesario por un error
				más aproiado.
		"""
		# Un usuario sin CVN accede a la URL de descarga introduciendo la misma de forma manual, se debe lanzar un 404.
		self.client.login(username = USERNAME, password = PASSWORD)		
		self.session = self.client.session
		self.session['attributes'] = ATTR
		self.session.save()	
		# TODO: Esto debería hacerlo el método tearDown ¿¿¿¿¿¿¿¿¿¿¿¿¿¿???????????????
		try:
			GrupoinvestInvestcvn.objects.get(pk=ID_TEST).delete()
		except ObjectDoesNotExist:
			pass # Caso de que quede el registro almacenado en la BBDD de test		
		# Descarga del CVN
		response = self.client.get(reverse('downloadCVN'))
		self.assertEqual(response.status_code, 404) # El usuario 'testCVN' no tiene ningún CVN subido
		self.client.logout()


	def test_download_cvn_user_withCVN(self):
		"""
			Test: Usuario registrado con CVN subido, accede a la descarga del mismo.
			
			Notas:
				200 OK:The request has succeeded.
		"""
		# Se añade un CVN ficticio al usuario creado para tests y se comprueba que pueda descargarlo
		user = User.objects.db_manager('portalinvestigador').create_user(pk=ID_TEST, username=ATTR['username'], password='', email=ATTR['email'])		
		data_invest = {}
		data_invest['pk'] = ID_TEST
		data_invest['nombre'] = ATTR['first_name']
		data_invest['nif'] = ATTR['NumDocumento']
		data_invest['email'] = ATTR['email']		
		data_invest['categoria'] = GrupoinvestCategoriainvestigador.objects.create(pk=ID_TEST,nombre='INVES')
		data_invest['cod_persona'] = 'INVES'		
		data_invest['user'] = AuthUser.objects.get(username = ATTR['username'])
		invest = GrupoinvestInvestigador.objects.create(**data_invest)
		invest_cvn = GrupoinvestInvestcvn.objects.create(pk = ID_TEST, investigador = invest, cvnfile = CVN_FILE)
		# Se loguea el usuario y procede a descargar su CVN
		self.client.login(username = USERNAME, password = PASSWORD)		
		self.session = self.client.session
		self.session['attributes'] = ATTR
		self.session.save()	
		# Se descarga el CVN		
		response = self.client.get(reverse('downloadCVN'))
		self.assertEqual(response.status_code, 200)	# Fichero descargado	
		self.client.logout()

	
	def test_login_redirect(self):
		"""
			Test: Usuario anónimo accede a la aplicación -> redirección hacia la página del acceso CAS.
			
			Notas:
				302 Found: The requested resource resides temporarily under a different URI.
		"""
		# Accede un usuario anónimo, tiene que ser redirigido a la página de acceso
		response = self.client.get(reverse('main'))#, follow=True)
		self.assertEqual(response.status_code, 302) # Se redirige hacia la página de acceso CAS
		self.assertEqual(response._headers['location'][1], TEST_LOGIN)
		
		
		
		
		

class FecytWSTest(TestCase):
	"""
		Tests Web Service Fecyt
	"""
	def setUp(self):
		"""
			Método que se ejecuta antes de cada test de la clase para la configuración inicial de los mismos
		"""				
		self.clientWS = suds.client.Client(URL_WS)
	
	
	def __checkDataPublicacion__(self, data = None, libro=False):
		"""
			Función auxiliar que comprueba que los datos de las publicación han sido introducidos en la BBDD
			
			Variables:
				* data: Registro de tipo publicación con todos los datos que debieron ser introducidos.
				* libro: Indica que la publicación se trata de un libro, con lo que no se mira el ISSN
		"""				
		if not data.titulo:
			return False
		if not data.nombre_publicacion:
			return False
		if not data.autores:
			return False
		if not data.fecha:
			return False
		if not data.volumen:
			return False
		if not data.numero:
			return False
		if not data.pagina_inicial:
			return False
		if not data.pagina_final:
			return False
		if not libro:
			if not data.issn:			
				return False
		return True			
			
			
	def __checkDataExpCientifica__(self, data=None, proyecto = False):
		"""
			Función auxiliar que se encarga de comprobar que los datos de los Proyectos y Convenios 
			son insertados correctamente.
			
			Variables:
			* data: Registro que contiene todos los datos que debieron ser introducidos.
			* proyecto: Indica si se trata de un proyecto (True) o convenio (False)
		"""					
		if not data.denominacion_del_proyecto:			
			return False
		if not data.fecha_de_inicio:
			return False
		if proyecto:
			if not data.fecha_de_fin:
				return False
		if not data.duracion_anyos:			
			return False
		if not data.duracion_meses:			
			return False
		if not data.duracion_dias:			
			return False
		if not data.autores:			
			return False
		if not data.cod_segun_financiadora:			
			return False
		if not data.ambito:			
			return False			
		if not data.otro_ambito:		
			return False
		return True
	
	
	def __checkDataTesis__(self, data = None):
		"""
			Función auxiliar que comprueba que los datos de una Tesis se han introducido correctamente en la BBDD.
			
			Variable:
			* data: Registro de tipo tesis que contiene todos los datos que debieron ser introducidos.
		"""
		if not data.titulo:
			return False
		if not data.universidad_que_titula:
			return False
		if not data.autor:
			return False
		if not data.codirector:
			return False
		if not data.fecha_de_lectura:
			return False
		return True
				
	
	def __checkDataCongreso__(self, data = None):
		"""
			Función auxiliar que comprueba que los datos de un congreso se han introducido correctamente en la BBDD.
		"""
		if not data.titulo:
			return False
		if not data.nombre_del_congreso:
			return False
		if not data.fecha_realizacion:
			return False
		if not data.fecha_finalizacion:
			return False
		if not data.ciudad_de_realizacion:
			return False
		if not data.ambito:
			return False
		if not data.otro_ambito:
			return False
		if not data.autores:
			return False
		return True
		
		
	def __checkPublicacion__(self, user = None):
		"""
			Función auxiliar que se encarga de comprobar que se han añadido los artículos correctos.
			
			Variables:
			* user: Usuario 'Test' propietario de la actividad científica.
		"""
		self.assertEqual(Publicacion.objects.filter(usuario = user, tipo_de_produccion__icontains="Capítulo").count(), 3)
		self.assertEqual(Publicacion.objects.filter(usuario = user, tipo_de_produccion__iexact="Artículo").count(), 2)				
		self.assertEqual(Publicacion.objects.filter(usuario = user, tipo_de_produccion__iexact="Libro").count(), 1)
		# Se comprueba que los datos del Artículo se han introducido en la BBDD
		articulo = Publicacion.objects.get(usuario = user, titulo__icontains="Artículo 1")
		self.assertTrue(self.__checkDataPublicacion__(articulo))
		capitulo = Publicacion.objects.get(usuario = user, titulo__icontains="Capítulo 1")
		self.assertTrue(self.__checkDataPublicacion__(capitulo))
		libro = Publicacion.objects.get(usuario = user, titulo__icontains="Libro 1")
		self.assertTrue(self.__checkDataPublicacion__(libro, True))
		return True
				
				
	
	
	def	test_cvn2xml(self):
		"""
			Test: Obtiene la respresentación XML de un CVN con formato Fecyt a través del WebService.
		"""				
		dataPDF   = binascii.b2a_base64(open(CVN_FILE).read())
		# Llamada al WebService del Fecyt
		resultXML = self.clientWS.service.cvnPdf2Xml(USER_WS, PASSWD_WS, dataPDF)
		self.assertEqual(resultXML.errorCode,0) # Formato CVN-XML del Fecyt
		# Almacena el fichero resultante
		dataXML = base64.b64decode(resultXML.cvnXml)
		fileXML = open(XML_FILE, "w").write(dataXML)
	
		
	def test_insertCVN(self):
		"""
			Test: Inserta los datos de un CVN en la BBDD			
		"""		
		try:
			fileXML = open(XML_FILE, "r")			
		except IOError:			
			# Si no existe el fichero XML con los datos del CVN, se ejecuta el test de llamada al Fecyt.
			self.test_cvn2xml()
			fileXML = open(XML_FILE, "r")		
		# NOTE: urlXML -> Ruta en el servidor donde estarán los ficheros PDFs y XMLs necesarios para los test
		xmlCVN = UtilidadesXMLtoBBDD(fileXML = fileXML.name.split('/')[-1]) 
		xmlCVN.insertarXML()
		user = Usuario.objects.get(documento='123456788A')
		
		# Número de publicaciones totales (Artículos, Capítulos de Libros y Libros)
		self.assertEqual(Publicacion.objects.filter(usuario = user).count(), 6)
		# Número de artículos, capítulos y libros por separado. Se comprueba también que se introducen sus datos correctamente.
		self.assertTrue(self.__checkPublicacion__(user))
		
		# Número de Proyectos y Convenios
		self.assertEqual(Proyecto.objects.filter(usuario = user).count(), 2)
		self.assertTrue(self.__checkDataExpCientifica__(Proyecto.objects.get(usuario = user, denominacion_del_proyecto="Proyecto 1"), True))
		self.assertEqual(Convenio.objects.filter(usuario = user).count(), 3)
		self.assertTrue(self.__checkDataExpCientifica__(Convenio.objects.get(usuario = user, denominacion_del_proyecto="Convenio 1")))
		
		# Número de Tesis
		self.assertEqual(TesisDoctoral.objects.filter(usuario = user).count(), 2)
		self.assertTrue(self.__checkDataTesis__(TesisDoctoral.objects.get(usuario = user, titulo="Tesis Doctoral 1")))
		
		# Número de congresos
		self.assertEqual(Congreso.objects.filter(usuario = user).count(), 3)
		self.assertTrue(self.__checkDataCongreso__(Congreso.objects.get(usuario = user, titulo="Congreso 1")))
