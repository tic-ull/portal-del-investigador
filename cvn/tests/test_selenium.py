# -*- encoding: utf-8 -*-
from cvn.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import LiveServerTestCase
from django.test import TestCase
from drivers import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from viinvDB.models import GrupoinvestInvestigador, GrupoinvestInvestcvn, AuthUser, GrupoinvestCategoriainvestigador

# TODO: Fichero settings para test
# ################################
from django.conf import settings as st
import os
import time

CHROME_DRIVER = "/home/luis/Descargas/chromedriver"

ID_TEST      = 99999
TEST_SERVER  = 'http://10.219.4.213:8000'

CVN_LOCATION            = os.path.join(st.PROJECT_ROOT, 'cvn/tests/CVN-invbecario.pdf')
CVN_NOT_FECYT_LOCATION  = os.path.join(st.PROJECT_ROOT, 'cvn/tests/CVN-invbecario-notFecyt.pdf')
CVN_FILE                = os.path.join(st.MEDIA_ROOT, 'cvn/pdf/CVN-test-709bddb1.pdf')
XML_FILE                = os.path.join(st.MEDIA_ROOT, 'cvn/xml/CVN-test-709bddb1.xml')

USER_LOGIN   = "invbecario"
USER_PASSWD  = "pruebasINV1"
USER_NIF     = "123456789A"

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
        #~ cls.selenium = WebDriver()
        cls.drivers = WebDriverList(
                webdriver.Chrome(CHROME_DRIVER),
                webdriver.Firefox(),
        )
        super(CVNTestCase, cls).setUpClass()


    @classmethod
    def tearDownClass(cls):
        """ Este método se ejecuta al final de la ejecución de todos los tests """
        cls.drivers.quit()
        super(CVNTestCase, cls).tearDownClass()
        #~ cls.selenium.quit()


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

    ####
    def assertNotRaises(self, excClass, callableObj=None, *args, **kwargs):
        """
            Fail if an exception of class excClass is thrown by
            callableObj when invoked with arguments args and keyword
            arguments kwargs.
        """
        try:
            callableObj(*args, **kwargs)
        except excClass:
            raise self.failureException("%s was raised" % excClass)
    ###

    @test_drivers()
    def test_01_login(self):
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


    @test_drivers()
    def test_02_login_cookie(self):
        """
            Acceso a la aplicación mediante un usuario de pruebas CAS. Se usan cookies para corroborar
            que el acceso se ha efectuado de manera correcta.
        """
        self.__inic_session__(USER_LOGIN, USER_PASSWD)
        cookie = self.selenium.get_cookies()
        self.assertIn(u"Bienvenido", cookie[1]['value'])
        time.sleep(2)
        self.selenium.find_element_by_link_text("Cerrar sesión").click()


    @test_drivers()
    def test_03_upload_cvn(self):
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


    @test_drivers()
    def test_04_upload_cvn_not_fecyt(self):
        """
            Accede a la aplicación e intenta subir un CVN que no tiene formato FECYT.
        """
        self.__inic_session__(USER_LOGIN, USER_PASSWD)
        # Una vez en la sesión procede a la subida de un CVN con formato Fecyt
        uploadCVN = self.selenium.find_element_by_xpath('//input[@name="cvnfile"]')
        time.sleep(2)
        uploadCVN.send_keys(CVN_NOT_FECYT_LOCATION)
        time.sleep(2)
        self.selenium.find_element_by_xpath('//button[.="Actualizar"]').click()
        try:
            upload = self.selenium.find_element_by_class_name("alert-error")
        except NoSuchElementException:
            upload = None
        time.sleep(4)
        self.assertIsNotNone(upload) # No se ha subido el CVN
        # TODO: Ver que ocurre, pues detecta el fichero como si no fuera un PDF        
        self.assertIn(u'no tiene formato FECYT', upload.text)        
        self.selenium.find_element_by_link_text("Cerrar sesión").click()


    @test_drivers()
    def test_05_download_cvn(self):
        """
            Accede a la aplicación y descarga el CVN que previamente se ha subido en el test 'test_upload_cvn'
        """
        self.__inic_session__(USER_LOGIN, USER_PASSWD)
        try:
            cvn = self.selenium.find_element_by_xpath('//a[@href="/investigacion/cvn/download/"]')
            time.sleep(2)
            cvn.click()
        except NoSuchElementException:
            cvn = None
            #~ self.selenium.get('%s%s' % (TEST_SERVER, reverse('downloadCVN')))
        # Comprueba que el usuario ha subido un CVN
        self.assertIsNotNone(cvn)
        # Comprobar que se abre el pdf. Se cambia a la ventana donde se abre el PDF
        self.selenium.switch_to_window(self.selenium.window_handles[1])
        time.sleep(2)
        self.assertIn('pdf', self.selenium.page_source)
        #~ if self.selenium.name == u'firefox':
            #~ self.assertIn(u'CVN -', self.selenium.title)
        #~ elif self.selenium.name == u'chrome':
            #~ self.assertIn(u"application/pdf", self.selenium.page_source)
        #~ self.assertNotRaises(Http404, lambda:self.selenium.switch_to_window(self.selenium.window_handles[1]))
        self.selenium.switch_to_window(self.selenium.window_handles[0])
        time.sleep(2)
        self.selenium.find_element_by_link_text("Cerrar sesión").click()


    @test_drivers()
    def test_06_login_no_user_CAS(self):
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
    fixtures = ['cvn/tests/fixtures/initial_data.json'] # Si no se especifica en el settings, la ruta de búsqueda es ./<app>/fixtures/
    selenium = None

    @classmethod
    def setup_invest(cls):
        """
            Método privado que crea un usuario en la BBDD del portal con un CVN de pruebas.
        """
        user = User.objects.db_manager('portalinvestigador').create_user(pk=1, username=USER_LOGIN, password='', email='')
        data_invest = {'pk':1,'nombre': user.first_name,'nif':USER_NIF,'email':user.email,
                    'categoria': GrupoinvestCategoriainvestigador.objects.create(pk=ID_TEST,nombre='INVES'),
                    'cod_persona':'INVES','user':AuthUser.objects.get(username = USER_LOGIN)}
        invest = GrupoinvestInvestigador.objects.create(**data_invest)
        invest_cvn = GrupoinvestInvestcvn.objects.create(pk = 1, investigador = invest, cvnfile = CVN_FILE)


    @classmethod
    def setUpClass(cls):
        #~ cls.selenium = webdriver.Firefox()#WebDriver()
        #~ cls.selenium = webdriver.Chrome(CHROME_DRIVER)
        # Lista de navegadores que van
        cls.drivers = WebDriverList(
                webdriver.Chrome(CHROME_DRIVER),
                webdriver.Firefox(),
        )
        super(AdminCVNTestCase, cls).setUpClass()
        # Se crea el usuario que se va a usar para los test 02 y 03
        cls.setup_invest()


    @classmethod
    def tearDownClass(cls):
        cls.drivers.quit()
        super(AdminCVNTestCase, cls).tearDownClass()
        #~ cls.selenium.quit()
        # Se elimina el fichero generado por la llamada al Fecyt
        try:
            os.remove(XML_FILE)
        except OSError:
            pass


    @test_drivers()
    def test_01_login(self):
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


    def test_02_callFecyt(self):
        """
            Realiza una llamada al Fecyt para obtener el XML correspondiente al CVN
        """
        # Login del administrador
        self.selenium.get("%s%s" % (self.live_server_url, '/investigacion/admin'))
        self.selenium.find_element_by_name("username").send_keys(ADMIN_LOGIN)
        self.selenium.find_element_by_name("password").send_keys(ADMIN_PASSWD)
        self.selenium.find_element_by_xpath('//input[@value="Iniciar sesión"]').click()
        # Accede al usuario test del cual se va a obtener la representación XML
        self.selenium.find_element_by_link_text("CVN Investigadores").click()
        time.sleep(2)
        self.selenium.find_element_by_xpath('//input[@value="1"]').click()
        self.selenium.find_element_by_xpath('//select[@name="action"]').click()
        # Seleccionar la opción que llama al Fecyt
        option = self.selenium.find_element_by_xpath('//option[@value="getAdminXML"]')
        option.click()
        option.submit()
        # Se comprueba que se ha obtenido el fichero XML y almacenado en el lugar correspondiente
        try:
            fileXML = open(XML_FILE, "r")
        except IOError:
            fileXML = None
        self.assertIsNotNone(fileXML)
        fileXML.close()


    def test_03_importData(self):
        """
            Realiza la importación de datos a partir del fichero XML
        """
        # Login
        self.selenium.get("%s%s" % (self.live_server_url, '/investigacion/admin'))
        self.selenium.find_element_by_name("username").send_keys(ADMIN_LOGIN)
        self.selenium.find_element_by_name("password").send_keys(ADMIN_PASSWD)
        self.selenium.find_element_by_xpath('//input[@value="Iniciar sesión"]').click()
        # Accede al usuario test del cual se va a obtener la representación XML
        self.selenium.find_element_by_link_text("CVN Investigadores").click()
        time.sleep(2)
        self.selenium.find_element_by_xpath('//input[@value="1"]').click()
        self.selenium.find_element_by_xpath('//select[@name="action"]').click()
        # Seleccionar la opción que importa el XML generado en el test 02
        option = self.selenium.find_element_by_xpath('//option[@value="parseAdminPDF"]')
        option.click()
        option.submit()
        # Comprobación de que se han introducido los datos
        self.assertEqual(TesisDoctoral.objects.count(), 2)
        self.assertEqual(Proyecto.objects.count(), 2)
        self.assertEqual(Convenio.objects.count(), 3)
        self.assertEqual(Congreso.objects.count(), 3)
        self.assertEqual(Publicacion.objects.count(), 6)

