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
		print self.live_server_url
		self.selenium.get('%s%s' % (self.live_server_url, '/investigacion/'))
		username_input = self.selenium.find_element_by_name("username")        
		username_input.send_keys('lcerrudo')
		password_input = self.selenium.find_element_by_name("password")
		print dir(self.selenium)
		password_input.send_keys('qn5LqUaj') 
		self.selenium.find_element_by_xpath('//input[@value="Iniciar sesión"]').click()
