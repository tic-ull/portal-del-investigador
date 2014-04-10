# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import CVN
from django.test import TestCase
from factories import UserFactory, AdminFactory
from django.core.files.base import ContentFile
from django.conf import settings as st
import datetime
from lxml import etree
import os


class CVNTestCase(TestCase):

    def setUp(self):
        self.xml_ull = open(os.path.join(stCVN.TEST_ROOT,
                            'xml/CVN-ULL.xml'), 'r')
        self.xml_empty = open(os.path.join(stCVN.TEST_ROOT,
                              'xml/empty.xml'), 'r')
        self.xml_test = open(os.path.join(stCVN.TEST_ROOT,
                             'xml/CVN-Test.xml'), 'r')

    def test_insert_xml_ull(self):
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

    def test_check_insert_data_congreso(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
            data = {}
            key = item.find('CvnItemID/CVNPK/Item').text.strip()
            if (key in stCVN.MODEL_TABLE and
               stCVN.MODEL_TABLE[key] == 'Congreso'):
                data = cvn._dataCongress(item)
                self.assertIn(u'titulo', data)
                self.assertEqual(data[u'titulo'], u'Título')
                self.assertIn(u'nombre_del_congreso', data)
                self.assertEqual(
                    data[u'nombre_del_congreso'], u'Nombre del congreso')
                self.assertIn(u'fecha_realizacion', data)
                self.assertEqual(data[u'fecha_realizacion'], u'2014-04-01')
                self.assertIn(u'fecha_finalizacion', data)
                self.assertEqual(data[u'fecha_finalizacion'], u'2014-04-05')
                self.assertIn(u'ciudad_de_realizacion', data)
                self.assertEqual(
                    data[u'ciudad_de_realizacion'], u'Ciudad de realización')
                self.assertIn(u'autores', data)
                self.assertEqual(data[u'autores'], u'STIC')
                self.assertIn(u'ambito', data)
                self.assertEqual(data[u'ambito'], u'Autonómica')
                break

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
            pdf_ull = open(os.path.join(stCVN.TEST_ROOT,
                           'cvn/CVN-ULL.pdf'), 'r')
            cvn = CVN()
            cvn.updated_at = datetime.datetime.now()
            cvn.cvn_file.save('CVN-ULL.pdf',
                              ContentFile(pdf_ull.read()),
                              save=False)
            cvn.backup_pdf()
            relative_path = ('cvn/old_cvn/CVN-ULL-' +
                             cvn.updated_at.strftime('%Y-%m-%d') + '.pdf')
            full_path = os.path.join(st.MEDIA_ROOT, relative_path)
            self.assertTrue(os.path.isfile(full_path))

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
