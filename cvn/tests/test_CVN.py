# -*- encoding: UTF-8 -*-

from django.test import TestCase
from cvn.models import CVN
from django.contrib.auth.models import User
from django.conf import settings as st
from factories import UserFactory, AdminFactory
import os


class CVNTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='rabadmar')
        xml = open(os.path.join(st.MEDIA_ROOT, 'cvn/xml/dyeray.xml'), 'r')
        self.example_xml = xml.read()
        self.fileXML = open(os.path.join(st.MEDIA_ROOT, 'cvn/xml/CVN-rabadmar.xml'), 'r')

    def test_insertXML(self):
        """ Insert the data of XML data in the database """
        try:
            cvn = CVN(xml_file=self.fileXML)
            cvn.insertXML(self.user.profile)
            self.assertEqual(self.user.profile.publicacion_set.filter(
                tipo_de_produccion='Articulo').count(), 0)
            self.assertEqual(self.user.profile.publicacion_set.filter(
                tipo_de_produccion='Libro').count(), 0)
            self.assertEqual(self.user.profile.publicacion_set.filter(
                tipo_de_produccion='Capitulo de Libro').count(), 0)
            self.assertEqual(self.user.profile.congreso_set.count(), 0)
            self.assertEqual(self.user.profile.convenio_set.count(), 0)
            self.assertEqual(self.user.profile.proyecto_set.count(), 1)
            self.assertEqual(self.user.profile.tesisdoctoral_set.count(), 0)
        except:
            raise

    def test_check_no_permission_to_upload_cvn(self):
        u = UserFactory.create()
        u.profile.documento = '00000000A'
        self.assertFalse(CVN.can_user_upload_cvn(u, self.example_xml))

    def test_admin_permission_to_upload_cvn(self):
        a = AdminFactory.create()
        self.assertTrue(CVN.can_user_upload_cvn(a, self.example_xml))

    def test_check_permission_to_upload_cvn(self):
        u = UserFactory.create()
        u.profile.documento = '78637064H'
        self.assertTrue(CVN.can_user_upload_cvn(u, self.example_xml))
