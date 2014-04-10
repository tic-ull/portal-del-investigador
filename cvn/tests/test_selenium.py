# -*- encoding: UTF-8 -*-

#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import Select
from django.conf import settings as st
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        NoAlertPresentException)
import unittest  # , time, re
import time


class LoginCAS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://loginpruebas.ull.es/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_login_cas(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "investigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invbecario")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def test_login_no_cas(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "investigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invNoCas")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
        time.sleep(2)
#        self.failUnless(driver.find_element_by_text(
#                        u"No se puede determinar que las credenciales" +
#                        "proporcionadas sean auténticas."))

    def test_upload_cvn_fecyt(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "investigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invbecario")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
#        driver.find_element_by_id("id_cvn_file").clear()
        driver.find_element_by_id(
            "id_cvn_file").send_keys(st.BASE_DIR +
                                     "/cvn/tests/files/cvn/CVN-Test-2.pdf")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def test_upload_cvn_no_fecyt(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "investigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invbecario")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
#        driver.find_element_by_id("id_cvn_file").clear()
        driver.find_element_by_id(
            "id_cvn_file").send_keys(st.BASE_DIR +
                                     "/cvn/tests/files/cvn/CVN-NO-FECYT.pdf")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def test_upload_cvn_user_admin(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "investigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invipas")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
#        driver.find_element_by_id("id_cvn_file").clear()
        driver.find_element_by_id(
            "id_cvn_file").send_keys(st.BASE_DIR +
                                     "/cvn/tests/files/cvn/CVN-Test.pdf")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def test_user_download_cvn(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "investigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invipas")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
#        driver.find_element_by_id("id_cvn_file").clear()
        driver.find_element_by_id(
            "id_cvn_file").send_keys(st.BASE_DIR +
                                     "/cvn/tests/files/cvn/CVN-Test.pdf")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:  # , e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException:  # , e:
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
