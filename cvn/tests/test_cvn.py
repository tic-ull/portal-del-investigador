# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import (CVN, Congreso, Publicacion, Convenio, Proyecto,
                        TesisDoctoral)
from cvn.parser_helpers import parse_produccion_type
from django.core.files.base import ContentFile
from django.test import TestCase
from factories import UserFactory, AdminFactory
from lxml import etree
import datetime
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
            user.profile.cvn = cvn
            cvn.insert_xml()
            self.assertEqual(user.profile.publicacion_set.filter(
                tipo_de_produccion='Articulo').count(), 1135)
            self.assertEqual(user.profile.publicacion_set.filter(
                tipo_de_produccion='Libro').count(), 6)
            self.assertEqual(user.profile.publicacion_set.filter(
                tipo_de_produccion='Capitulo').count(), 32)
            self.assertEqual(user.profile.congreso_set.count(), 55)
            self.assertEqual(user.profile.convenio_set.count(), 38)
            self.assertEqual(user.profile.proyecto_set.count(), 11)
            self.assertEqual(user.profile.tesisdoctoral_set.count(), 0)
        except:
            raise

    def test_check_read_data_congress(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
            data = {}
            tipo = parse_produccion_type(item)
            if tipo == 'Congreso':
                data = Congreso.objects.create(item, None, False)
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

    def test_check_read_data_publication(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
            tipo = parse_produccion_type(item)
            if tipo == 'Publicacion':
                data = Publicacion.objects.create(item, None, False)
                self.assertIn(u'tipo_de_produccion', data)
                self.assertIn(
                    data[u'tipo_de_produccion'],
                    ['Articulo', 'Capitulo', 'Libro'])
                self.assertIn(u'titulo', data)
                self.assertIn(u'nombre_publicacion', data)
                self.assertIn(u'autores', data)
                if data['tipo_de_produccion'] == 'Articulo':
                    self.assertEqual(data[u'titulo'], u'TÍTULO')
                    self.assertEqual(
                        data[u'nombre_publicacion'], u'NOMBRE')
                    self.assertEqual(data[u'autores'], u'STIC; STIC2')
                else:
                    self.assertEqual(
                        data[u'titulo'], u'Título de la publicación')
                    self.assertEqual(
                        data[u'nombre_publicacion'],
                        u'Nombre de la publicación')
                    if data['tipo_de_produccion'] == 'Libro':
                        self.assertEqual(data[u'autores'], u'STIC')
                    else:
                        self.assertEqual(data[u'autores'], u'Firma')
                self.assertIn(u'volumen', data)
                self.assertEqual(data[u'volumen'], u'1')
                self.assertIn(u'numero', data)
                self.assertEqual(data[u'numero'], u'1')
                self.assertIn(u'pagina_inicial', data)
                self.assertEqual(data[u'pagina_inicial'], u'1')
                self.assertIn(u'pagina_final', data)
                self.assertEqual(data[u'pagina_final'], u'100')
                self.assertIn(u'fecha', data)
                self.assertEqual(data[u'fecha'], u'2014-04-01')
                if data['tipo_de_produccion'] != 'Libro':
                    self.assertIn(u'issn', data)
                    self.assertEqual(data[u'issn'], u'0395-2037')

    def test_check_read_data_project(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
            tipo = parse_produccion_type(item)
            if tipo == 'Proyecto' or tipo == 'Convenio':
                data = {}
                if tipo == 'Proyecto':
                    data = Proyecto.objects.create(item, None, False)
                elif tipo == 'Convenio':
                    data = Convenio.objects.create(item, None, False)
                self.assertIn(u'denominacion_del_proyecto', data)
                self.assertEqual(
                    data[u'denominacion_del_proyecto'],
                    u'Denominación del proyecto')
                self.assertIn(u'fecha_de_inicio', data)
                self.assertEqual(data[u'fecha_de_inicio'], u'2014-04-01')
                if u'fecha_de_fin' in data:
                    self.assertEqual(data[u'fecha_de_fin'], u'2014-04-05')
                else:
                    if (u'duracion_anyos' in data and
                       u'duracion_meses' in data and
                       u'duracion_dias' in data):
                        self.assertEqual(data[u'duracion_anyos'], u'1')
                        self.assertEqual(data[u'duracion_meses'], u'1')
                        self.assertEqual(data[u'duracion_dias'], u'1')
                self.assertIn(u'autores', data)
                self.assertIn(u'ambito', data)
                if tipo == 'Proyecto':
                    self.assertEqual(data[u'autores'], u'Firma')
                    self.assertEqual(data[u'ambito'], u'Internacional no UE')
                else:
                    self.assertEqual(data[u'autores'], u'STIC')
                    self.assertEqual(data[u'ambito'], u'Autonómica')
                self.assertIn(u'cod_segun_financiadora', data)
                self.assertEqual(
                    data[u'cod_segun_financiadora'],
                    u'Cód. según financiadora')
                self.assertIn(u'cuantia_total', data)
                self.assertEqual(data[u'cuantia_total'], u'1')
                self.assertIn(u'cuantia_subproyecto', data)
                self.assertEqual(data[u'cuantia_subproyecto'], u'1')
                self.assertIn(u'porcentaje_en_subvencion', data)
                self.assertEqual(data[u'porcentaje_en_subvencion'], u'1')
                self.assertIn(u'porcentaje_en_credito', data)
                self.assertEqual(data[u'porcentaje_en_credito'], u'1')
                self.assertIn(u'porcentaje_mixto', data)
                self.assertEqual(data[u'porcentaje_mixto'], u'1')

    def test_check_read_data_tesis(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
            data = {}
            tipo = parse_produccion_type(item)
            if tipo == 'TesisDoctoral':
                data = TesisDoctoral.objects.create(item, None, False)
                self.assertIn(u'titulo', data)
                self.assertEqual(data[u'titulo'], u'Título del trabajo')
                self.assertIn(u'universidad_que_titula', data)
                self.assertEqual(
                    data[u'universidad_que_titula'],
                    u'Universidad que titula')
                self.assertIn(u'autor', data)
                self.assertEqual(data[u'autor'], u'Firma')
                self.assertIn(u'codirector', data)
                self.assertEqual(data[u'codirector'], u'Firma')
                self.assertIn(u'fecha_de_lectura', data)
                self.assertEqual(data[u'fecha_de_lectura'], u'2014-04-01')

    def test_on_insert_cvn_old_pdf_is_moved(self):
            pdf_ull = open(os.path.join(stCVN.TEST_ROOT,
                           'cvn/CVN-ULL.pdf'), 'r')
            cvn = CVN()
            cvn.updated_at = datetime.datetime.now()
            cvn.cvn_file.save('CVN-ULL.pdf',
                              ContentFile(pdf_ull.read()),
                              save=False)
            relative_path = (
                cvn.cvn_file.name.split('/')[-1].split('.')[0] + '-' +
                cvn.updated_at.strftime('%Y-%m-%d') + '.pdf')
            cvn._backup_pdf()
            full_path = os.path.join(stCVN.OLD_PDF_ROOT, relative_path)
            self.assertTrue(os.path.isfile(full_path))

    def test_check_no_permission_to_upload_cvn(self):
        u = UserFactory.create()
        u.profile.documento = '12345678A'
        example_xml = self.xml_test.read()
        self.assertFalse(CVN.can_user_upload_cvn(u, example_xml))

    def test_admin_permission_to_upload_cvn(self):
        a = AdminFactory.create()
        example_xml = self.xml_test.read()
        self.assertTrue(CVN.can_user_upload_cvn(a, example_xml))

    def test_check_permission_to_upload_cvn(self):
        u = UserFactory.create()
        u.profile.documento = '00000000A'
        example_xml = self.xml_test.read()
        self.assertTrue(CVN.can_user_upload_cvn(u, example_xml))
