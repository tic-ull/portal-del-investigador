# -*- encoding: UTF-8 -*-

#
#    Copyright 2014-2015
#
#      STIC-Investigación - Universidad de La Laguna (ULL) <gesinv@ull.edu.es>
#
#    This file is part of CVN.
#
#    CVN is free software: you can redistribute it and/or modify it under
#    the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    CVN is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with CVN.  If not, see
#    <http://www.gnu.org/licenses/>.
#

from core.tests.helpers import init, clean
from django import test
from django.conf import settings as st

from core.models import UserProfile
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display


class LoginCAS(test.LiveServerTestCase):

    def __init__(self, *args, **kwargs):
        super(LoginCAS, self).__init__(*args, **kwargs)
        init()

    def setUp(self):
        #display = Display(visible=0, size=(1280, 1024))
        #display.start()
        #self.display = display
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(8)
        self.driver.set_page_load_timeout(30)
        self.base_url = st.CAS_SERVER_URL
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_selenium_cambio_correcto_dni(self):
        user = UserProfile.get_or_create_user('invipas', '72693103Q')[0]
        user.set_password("pruebasINV1")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        driver = self.driver
        driver.get(self.base_url + "/cas-1/login?service=http%3A%2F%2Flocalhost"
                                   "%3A8081%2Finvestigacion%2Faccounts%2Flogin"
                                   "%2F%3Fnext%3D%252Finvestigacion%252Fadmin"
                                   "%252Flogin%252F%253Fnext%253D%252F"
                                   "investigacion%252Fadmin%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invipas")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
        driver.find_element_by_link_text("User profiles").click()
        driver.find_element_by_id("searchbar").clear()
        driver.find_element_by_id("searchbar").send_keys(user.username)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("tr.row1 > td.action-checkbox > "
                                            "input[name=\"_selected_action\"]"
                                            ).click()
        Select(driver.find_element_by_name("action")
               ).select_by_visible_text("Change user's DNI")
        driver.find_element_by_name("index").click()
        driver.find_element_by_id("id_new_dni").clear()
        driver.find_element_by_id("id_new_dni").send_keys("08030254B")
        driver.find_element_by_name("apply").click()
        try:
            result = driver.find_element_by_class_name("info").text
        except NoSuchElementException:
            result = ''
        self.assertTrue((u'Successfully changed dni.' in result))

    def test_selenium_cambio_incorrecto_dni(self):
        user = UserProfile.get_or_create_user('invipas', '72693103Q')[0]
        user.set_password("pruebasINV1")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        driver = self.driver
        driver.get(self.base_url + "/cas-1/login?service=http%3A%2F%2Flocalhost"
                                   "%3A8081%2Finvestigacion%2Faccounts%2Flogin"
                                   "%2F%3Fnext%3D%252Finvestigacion%252Fadmin"
                                   "%252Flogin%252F%253Fnext%253D%252F"
                                   "investigacion%252Fadmin%252F")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invipas")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pruebasINV1")
        driver.find_element_by_name("submit").click()
        driver.find_element_by_link_text("User profiles").click()
        driver.find_element_by_id("searchbar").clear()
        driver.find_element_by_id("searchbar").send_keys(user.username)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("tr.row1 > td.action-checkbox > "
                                            "input[name=\"_selected_action\"]"
                                            ).click()
        Select(driver.find_element_by_name("action")
               ).select_by_visible_text("Change user's DNI")
        driver.find_element_by_name("index").click()
        driver.find_element_by_id("id_new_dni").clear()
        driver.find_element_by_id("id_new_dni").send_keys("88888888B")
        driver.find_element_by_name("apply").click()
        try:
            result = driver.find_element_by_class_name("info").text
        except NoSuchElementException:
            result = ''
        self.assertFalse(u'Successfully changed dni.' in result)

    def tearDown(self):
        self.driver.quit()
        #self.display.stop()
        self.assertEqual([], self.verificationErrors)

    @classmethod
    def tearDownClass(cls):
        clean()
