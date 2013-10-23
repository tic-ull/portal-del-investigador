# -*- encoding: utf-8 -*-
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

    
class MySeleniumTests(LiveServerTestCase):
	fixtures = ['user-data.json']
	
	@classmethod
	def setUpClass(cls):
		cls.selenium = WebDriver()
		super(MySeleniumTests, cls).setUpClass()
		
		

	@classmethod        
	def tearDownClass(cls):
		cls.selenium.quit()
		super(MySeleniumTests, cls).tearDownClass()

	def test_login(self):		
		self.selenium.get('%s%s' % ('http://10.219.4.213:8000','/investigacion/'))
		#~ self.selenium.get('%s%s' % (self.live_server_url, '/investigacion/'))
		username_input = self.selenium.find_element_by_name("username")        
		username_input.send_keys('invbecario')
		password_input = self.selenium.find_element_by_name("password")
		print dir(self.selenium)
		password_input.send_keys('pruebasINV1') 
		response = self.selenium.find_element_by_xpath('//input[@value="Iniciar sesión"]').click()
		print response
		print dir(response)
