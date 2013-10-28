# -*- encoding: utf-8 -*-

# Tests
from django.test import LiveServerTestCase
from django.test import TestCase

# Selenium
from selenium.webdriver.firefox.webdriver import WebDriver

# Llamada a las vistas
from django.core.urlresolvers import reverse

# Excepción para la búsqueda de elementos en páginas
from selenium.common.exceptions import NoSuchElementException
	
# Excepción para la búsqueda de objetos en la BBDD
from django.core.exceptions import ObjectDoesNotExist

# TODO: Fichero settings para test
# ################################
from django.conf import settings as st

import os
import time

TEST_SERVER  = 'http://10.219.4.213:8000'
CVN_LOCATION = os.path.join(st.PROJECT_PATH, 'cvn/tests/CVN-invbecario.pdf')
USER_LOGIN   = "invbecario"
USER_PASSWD  = "pruebasINV1"
ADMIN_LOGIN  = "admin"
ADMIN_PASSWD = "123"
# ################################
#~ class MySeleniumTests(LiveServerTestCase):
class CVNTestCase(TestCase):
	"""
		Clase que contiene los test para corroborar el correcto funcionamiento de las siguientes funcionalidades (usuario):
		- Acceso a la aplicación por medio de un usuario CAS de pruebas.
		- Subida de un CVN a la aplicación con formato Fecyt.
		- Descarga de un CVN a la aplicación.
		- Acceso a la aplicación por parte de un usuario no registrado en el CAS.
	"""
		
	@classmethod		
	def setUpClass(cls):
		cls.selenium = WebDriver()
		super(CVNTestCase, cls).setUpClass()
		
		
	@classmethod        
	def tearDownClass(cls):
		cls.selenium.quit()
		super(CVNTestCase, cls).tearDownClass()
		

	def __inic_session__(self, login = None, passwd = None):
		"""
			Método privado que inicia la sesión en la aplicación con el usuario indicado como parámetro.
			
			Variables:
			* login: Nombre de usuario.
			* passwd: Contraseña.
		"""
		# Incio de sesión se aplica en todos los tests		
		self.selenium.get('%s%s' % (TEST_SERVER, reverse('main')))
		#~ self.selenium.get('%s%s' % (self.live_server_url, '/investigacion/'))
		username_input = self.selenium.find_element_by_name("username")        
		username_input.send_keys(login)
		time.sleep(2)		
		password_input = self.selenium.find_element_by_name("password")
		password_input.send_keys(passwd) 
		time.sleep(2)		
		self.selenium.find_element_by_xpath('//input[@value="Iniciar sesión"]').click()


	def test_login(self):
		"""
			Acceso a la aplicación mediante un usuario de pruebas CAS. Se busca el elemento de cierre de la sesión
			para corroborar que se ha accedido correctamente.
		"""		
		
		self.__inic_session__(USER_LOGIN, USER_PASSWD)
		try:
			close_session = self.selenium.find_element_by_link_text("Cerrar sesión")
		except NoSuchElementException:
			close_session = None
		#self.assertEqual(self.selenium.find_element_by_class_name("main-title").text, u"Currículum Vítae Normalizado (CVN)")
		self.assertIsNotNone(close_session)
		time.sleep(2)
		self.selenium.find_element_by_link_text("Cerrar sesión").click()
		
		
	def test_login_cookie(self):
		"""
			Acceso a la aplicación mediante un usuario de pruebas CAS. Se usan cookies para corroborar 
			que el acceso se ha efectuado de manera correcta.
		"""		
		self.__inic_session__(USER_LOGIN, USER_PASSWD)
		cookie = self.selenium.get_cookies()				
		self.assertIn(u"Bienvenido", cookie[1]['value'])
		time.sleep(2)
		self.selenium.find_element_by_link_text("Cerrar sesión").click()		
		

	def test_upload_cvn(self):
		"""
			Accede a la aplicación y sube un CVN.
		"""
		self.__inic_session__(USER_LOGIN, USER_PASSWD)		
		# Una vez en la sesión procede a la subida de un CVN con formato Fecyt
		uploadCVN = self.selenium.find_element_by_xpath('//input[@name="cvnfile"]')
		uploadCVN.send_keys(CVN_LOCATION)
		self.selenium.find_element_by_xpath('//button[.="Actualizar"]').click()
		# Comprobar que se ha subido con éxito
		try:
			upload = self.selenium.find_element_by_xpath('//table/tbody/tr/td/strong[.="Actualizado"]')
		except NoSuchElementException:
			upload = None
		self.assertIsNotNone(upload)
		time.sleep(2)
		self.selenium.find_element_by_link_text("Cerrar sesión").click()


	def test_download_cvn(self):
		"""
			Accede a la aplicación y descarga el CVN que previamente se ha subido en el test 'test_upload_cvn'
		"""
		self.__inic_session__(USER_LOGIN, USER_PASSWD)		
		try:
			cvn = self.selenium.find_element_by_xpath('//a[@href="/investigacion/cvn/download/"]')
			cvn.click()
			time.sleep(2)
		except NoSuchElementException:
			cvn = None
		# Comprueba que el usuario ha subido un CVN
		self.assertIsNotNone(cvn)		
		# Comprobar que se abre el pdf. Se cambia a la ventana donde se abre el PDF		
		self.selenium.switch_to_window(self.selenium.window_handles[1])		
		time.sleep(2)
		self.assertIn(u"CVN -", self.selenium.title)
		self.selenium.switch_to_window(self.selenium.window_handles[0])
		self.selenium.find_element_by_link_text("Cerrar sesión").click()
		
	
	def test_login_no_user_CAS(self):
		"""
			Realiza una comprobación de que un usuario no CAS no puede acceder a la página
		"""
		self.__inic_session__("NOCAS", "NOCAS")
		msg_alert = self.selenium.find_element_by_xpath('//div[@id="status"]').text
		self.assertIn(u'No se puede determinar que las credenciales proporcionadas', msg_alert)
	



class AdminCVNTestCase(LiveServerTestCase):
	"""
		Clase que contiene los test para comprobar el correcto funcionamiento de las funcionalidades 
		de la plantilla de administración:
		- Acceso a la plantilla administrador mediante un usuario con permisos de 'staff'.
	"""
	
	fixtures = ['initial-data.json'] # Si no se especifica en el settings, la ruta de búsqueda es ./<app>/fixtures/
	
	@classmethod		
	def setUpClass(cls):
		cls.selenium = WebDriver()
		super(AdminCVNTestCase, cls).setUpClass()
		
		
	@classmethod        
	def tearDownClass(cls):
		cls.selenium.quit()
		super(AdminCVNTestCase, cls).tearDownClass()
	
	
	def test_login(self):		
		"""
			Comprueba se puede acceder a la plantilla de administración correctamente con un usuario STAFF		
		"""
		self.selenium.get("%s%s" % (self.live_server_url, '/investigacion/admin'))
		username_input = self.selenium.find_element_by_name("username")
		username_input.send_keys(ADMIN_LOGIN)
		time.sleep(2)
		password_input = self.selenium.find_element_by_name("password")
		password_input.send_keys(ADMIN_PASSWD) 
		time.sleep(2)
		ini_session = self.selenium.find_element_by_xpath('//input[@value="Iniciar sesión"]')
		ini_session.click()
		self.assertTrue(self.selenium.find_element_by_id('user-tools').text.startswith('Bienvenido'))
		
