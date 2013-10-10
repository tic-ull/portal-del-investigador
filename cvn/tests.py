"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

#~ from django.test import LiveServerTestCase
#~ from selenium.webdriver.firefox.webdriver import WebDriver
#~ 
#~ class MySeleniumTests(LiveServerTestCase):
    #~ fixtures = ['user-data.json']
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
        #~ self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        #~ username_input = self.selenium.find_element_by_name("username")
        #~ username_input.send_keys('myuser')
        #~ password_input = self.selenium.find_element_by_name("password")
        #~ password_input.send_keys('secret')
        #~ self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

