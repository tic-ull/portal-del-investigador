# -*- encoding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Constantes para los tests
USERNAME = 'testCVN'
PASSWORD = '123'
EMAIL    = 'test@ull.edu.es'
ATTR     = {'username': 'testCVN', 'first_name': 'Test', 'last_name': 'Testing CVN', 
			'TipoDocumento': 'NIF', 'NumDocumento': '123456789V', 
			'ou': ['PDI', 'srv_wifi', 'Alumnos', 'srv_soft', 'rol_becario', 'srv_webpages', 'srv_ddv', 
					'srv_vpn', 'CCTI', 'srv_siga_ull.es', 'NACFicheros', 'Act', 'srv_google', 'srv_siga'],
			'email': 'test@ull.edu.es'}

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class UserAccessTest(TestCase):
	"""
		Test de pruebas usando "Client". 
	"""
	def setUp(self):
		self.user = User.objects.create(username=USERNAME, email=EMAIL)
		# Se añade la clave con el cifrado utilizado por Django
		self.user.set_password(PASSWORD)
		self.user.save()		
		self.client = Client()

		
	def test_login(self):				
		# El usuario creado se puede loguear.
		result = self.client.login(username = USERNAME, password = PASSWORD)
		self.assertTrue(result)
		# Sale de la sesión
		self.client.logout()
		

	def test_login_redirect(self):
		# Accede un usuario anónimo, tiene que ser redirigido a la página de acceso
		result = self.client.get(reverse('main'), follow=True)
		# TODO FALLA, el status_code es el problema !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		self.assertRedirects(result, 'http://testserver/investigacion/accounts/login/')
		

class FuncionalityTest(TestCase):
	"""
		Test 
	"""
	def setUp(self):
		# Se crea un usuario y se accede a la aplicación
		self.user = User.objects.create(username=USERNAME, email=EMAIL)					
		self.user.set_password(PASSWORD)		
		self.user.save()	
		
		# Accede a la aplicación
		self.client.login(username = USERNAME, password = PASSWORD)
		self.client = Client()
		
		# Al ser un usuario local, se añaden los atributos que debería recibir por el CAS en la sesión
		self.session = self.client.session
		self.session['attributes'] = ATTR
		self.session.save()		
		
		
	def test_main_page(self):
		
		
		# Acceso a la página principal
		print self.session['attributes']
		result = self.client.get(reverse("index"))
		print result.status_code








#~ from django.test import LiveServerTestCase
#~ from selenium.webdriver.firefox.webdriver import WebDriver
#~ 
    #~ fixtures = ['user-data.json']
#~ class MySeleniumTests(LiveServerTestCase):
#~ 
    #~ @classmethod
    #~ def setUpClass(cls):
        #~ cls.selenium = WebDriver()
        #~ super(MySeleniumTests, cls).setUpClass()
#~ 
    #~ @classmethod        
    #~ def tearDownClass(cls):
        #~ cls.selenium.quit()
        #~ super(MySeleniumTests, cls).tearDownClass()
#~ 
    #~ def test_login(self):
        #~ print self.live_server_url
        #~ self.selenium.get('%s%s' % (self.live_server_url, '/investigacion/'))
        #~ username_input = self.selenium.find_element_by_name("username")        
        #~ username_input.send_keys('lcerrudo')
        #~ password_input = self.selenium.find_element_by_name("password")
        #~ print dir(self.selenium)
        #~ password_input.send_keys('qn5LqUaj') 
        #~ self.selenium.find_element_by_xpath('//input[@value="Iniciar sesión"]').click()
        

