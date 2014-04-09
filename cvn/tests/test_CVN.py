# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import CVN
from django.test import TestCase
from factories import UserFactory, AdminFactory
import os


class CVNTestCase(TestCase):

    def setUp(self):
        self.xml_ull = open(os.path.join(stCVN.TEST_ROOT, 'xml/CVN-ULL.xml'), 'r')
        self.xml_empty =  open(os.path.join(stCVN.TEST_ROOT, 'xml/empty.xml'), 'r')

    def test_insertXML_ULL(self):
        """ Insert the data of XML in the database """
        try:
            cvn = CVN(xml_file=self.xml_ull)
            user = UserFactory.create()
            cvn.insertXML(user.profile)
            self.assertEqual(user.profile.publicacion_set.filter(
                tipo_de_produccion='Articulo').count(), 1135)
            self.assertEqual(user.profile.publicacion_set.filter(
                tipo_de_produccion='Libro').count(), 6)
            self.assertEqual(user.profile.publicacion_set.filter(
                tipo_de_produccion='Capitulo de Libro').count(), 32)
            self.assertEqual(user.profile.congreso_set.count(), 55)
            self.assertEqual(user.profile.convenio_set.count(), 38)
            self.assertEqual(user.profile.proyecto_set.count(), 11)
            self.assertEqual(user.profile.tesisdoctoral_set.count(), 0)
        except:
            raise

    def test_on_insert_cvn_old_production_tables_are_deleted(self):
        try:
            u = UserFactory.create()
            cvn = CVN(xml_file=self.xml_ull)
            cvn.insertXML(u.profile)
            publicaciones = u.profile.publicacion_set.all()
            congresos = u.profile.congreso_set.all()
            convenios = u.profile.convenio_set.all()
            proyectos = u.profile.proyecto_set.all()
            tesis = u.profile.tesisdoctoral_set.all()
            cvn.xml_file = self.xml_empty
            cvn.insertXML(u.profile)
            self.assertEqual(publicaciones.count(), 0)
            self.assertEqual(congresos.count(), 0)
            self.assertEqual(convenios.count(), 0)
            self.assertEqual(proyectos.count(), 0)
            self.assertEqual(tesis.count(), 0)
        except:
            raise

    def test_on_insert_cvn_old_pdf_is_moved(self):
        try:
            u = UserFactory.create()
            cvn = CVN(xml_file=self.xml_ull)
            cvn.insertXML(u.profile)
            # Get pdf path

            cvn.xml_file = self.xml_empty
            cvn.insertXML(u.profile)
            # Check new pdf exists
        except:
            raise

    def test_check_no_permission_to_upload_cvn(self):
        u = UserFactory.create()
        u.profile.documento = '12345678A'
        example_xml = self.xml_ull.read()
        self.assertFalse(CVN.can_user_upload_cvn(u, example_xml))

    def test_admin_permission_to_upload_cvn(self):
        a = AdminFactory.create()
        example_xml = self.xml_ull.read()
        self.assertTrue(CVN.can_user_upload_cvn(a, example_xml))

    def test_check_permission_to_upload_cvn(self):
        u = UserFactory.create()
        u.profile.documento = '00000000A'
        example_xml = self.xml_ull.read()
        self.assertTrue(CVN.can_user_upload_cvn(u, example_xml))
