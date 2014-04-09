# -*- encoding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class LoginCAS(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://loginpruebas.ull.es/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_login_cas(self):
        driver = self.driver
        driver.get(self.base_url + "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2Finvestigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252Finvestigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invbecario")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def test_login_no_cas(self):
        driver = self.driver
        driver.get(self.base_url + "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2Finvestigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252Finvestigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invNoCas")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()

    def test_upload_cvn_fecyt(self):
        driver = self.driver
        driver.get(self.base_url + "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2Finvestigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252Finvestigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("lcerrudo")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("qn5LqUaj")
        driver.find_element_by_name("submit").click()
#        driver.find_element_by_id("id_cvn_file").clear()
        driver.find_element_by_id("id_cvn_file").send_keys("/home/luis/AppsStic/portalCVN/portalInv/cvn/tests/files/cvn/CVN-test.pdf")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def test_upload_cvn_no_fecyt(self):
        driver = self.driver
        driver.get(self.base_url + "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2Finvestigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252Finvestigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("lcerrudo")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("qn5LqUaj")
        driver.find_element_by_name("submit").click()
#        driver.find_element_by_id("id_cvn_file").clear()
        driver.find_element_by_id("id_cvn_file").send_keys("/home/luis/AppsStic/portalCVN/portalInv/cvn/tests/files/cvn/NO_FECYT.pdf")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException, e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
