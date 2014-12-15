# -*- encoding: UTF-8 -*-

from core.tests.helpers import init, clean
from cvn import settings as st_cvn
from django import test
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        NoAlertPresentException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import unittest
from pyvirtualdisplay import Display


class LoginCAS(test.LiveServerTestCase):

    def __init__(self, *args, **kwargs):
        super(LoginCAS, self).__init__(*args, **kwargs)
        init()

    def setUp(self):
        display = Display(visible=0, size=(1280, 1024))
        display.start()
        self.display = display
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(8)
        #self.driver.set_page_load_timeout(30)
        self.base_url = "https://loginpruebas.ull.es/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_login_cas(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "es%252Finvestigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invbecario")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
        self.assertTrue(self.is_element_present(By.CLASS_NAME, "page-header"))
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def test_login_no_cas(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "es%252Finvestigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invNoCas")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
        self.assertTrue(self.is_element_present(By.ID, "status"))

    def test_upload_cvn_fecyt(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "es%252Finvestigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invbecario")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
#        driver.find_element_by_id("id_cvn_file").clear()
        driver.execute_script(
            'document.getElementById("id_cvn_file").removeAttribute("style")')
        driver.find_element_by_id(
            "id_cvn_file").send_keys(st_cvn.TEST_ROOT + "cvn/CVN-Test_2.pdf")
        #driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertTrue(self.is_element_present(By.CLASS_NAME,
                                                "alert-success"))
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def test_upload_cvn_no_fecyt(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "es%252Finvestigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invbecario")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
        # driver.find_element_by_id("id_cvn_file").clear()
        driver.execute_script(
            'document.getElementById("id_cvn_file").removeAttribute("style")')
        driver.find_element_by_id("id_cvn_file").send_keys(
            st_cvn.TEST_ROOT + "cvn/CVN-NO-FECYT.pdf")
        #driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertTrue(self.is_element_present(By.CLASS_NAME,
                                                "errorlist"))
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def test_upload_cvn_user_admin(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "es%252Finvestigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invipas")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
        # Add admin permissions after login CAS
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'btn-signout')))
        u = User.objects.get(username="invipas")
        u.is_staff = True
        u.is_superuser = True
        u.save()
#        driver.find_element_by_id("id_cvn_file").clear()
        driver.execute_script(
            'document.getElementById("id_cvn_file").removeAttribute("style")')
        driver.find_element_by_id("id_cvn_file").send_keys(
            st_cvn.TEST_ROOT + "cvn/CVN-Test.pdf")
        #driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertTrue(self.is_element_present(By.CLASS_NAME,
                                                "alert-success"))
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def test_user_download_cvn(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "es%252Finvestigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invbecario")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
        # First upload CVN
        driver.execute_script(
            'document.getElementById("id_cvn_file").removeAttribute("style")')
        driver.find_element_by_id("id_cvn_file").send_keys(
            st_cvn.TEST_ROOT + "cvn/CVN-Test_2.pdf")
        #driver.find_element_by_xpath("//button[@type='submit']").click()
        # Download CVN
        driver.find_element_by_link_text(
            u'Descargar una copia de mi CVN').click()
        # Check if CVN window is open
        self.assertEqual(len(driver.window_handles), 2)
        # Change to CVN window
        driver.switch_to_window(driver.window_handles[-1])
        # Return to 'Main' windows
        driver.switch_to_window(driver.window_handles[0])
        driver.find_element_by_link_text(u"Cerrar sesión").click()

    def test_user_rrhh(self):
        driver = self.driver
        driver.get(self.base_url +
                   "/cas-1/login?service=http%3A%2F%2Flocalhost%3A8081%2F" +
                   "investigacion%2Faccounts%2Flogin%2F%3Fnext%3D%252F" +
                   "es%252Finvestigacion%252Fcvn%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invbecario")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
        driver.execute_script(
            'document.getElementById("id_cvn_file").removeAttribute("style")')
        driver.find_element_by_id(
            "id_cvn_file").send_keys(st_cvn.TEST_ROOT + "cvn/CVN-Test_2.pdf")
        self.assertFalse(self.is_element_present(By.ID, "dept"))
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
        self.display.stop()
        self.assertEqual([], self.verificationErrors)

    @classmethod
    def tearDownClass(cls):
        clean()

if __name__ == "__main__":
    unittest.main()
