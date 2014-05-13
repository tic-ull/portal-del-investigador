# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import (CVN, Congreso, Publicacion, Convenio, Proyecto,
                        TesisDoctoral, Articulo)
from cvn.parser_helpers import parse_produccion_type
from django.core.files.base import ContentFile
from django.test import TestCase
from core.tests.factories import UserFactory
from lxml import etree
from django.core.files.uploadedfile import SimpleUploadedFile
from cvn.forms import UploadCVNForm
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
            cvn.xml_file.seek(0)
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

    def test_number_of_articles(self):
        cvn = CVN(xml_file=self.xml_ull)
        cvn.xml_file.seek(0)
        u = UserFactory.create()
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        count = 0
        for item in items:
            cvn_key = item.find('CvnItemID/CVNPK/Item').text.strip()
            try:
                subtype = item.find('Subtype/SubType1/Item').text.strip()
            except AttributeError:
                subtype = ''
            if cvn_key == '060.010.010.000' and subtype == '035':
                count = count + 1
                Articulo.objects.create(item, u.profile)
        self.assertEqual(count, 1214)
        self.assertEqual(Articulo.objects.all().count(), 1135)

    def test_check_read_data_congress(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        u = UserFactory.create()
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
            data = {}
            tipo = parse_produccion_type(item)
            if tipo == 'Congreso':
                data = Congreso.objects.create(item, u.profile)
                self.assertEqual(data.titulo, u'Título')
                self.assertEqual(data.nombre_del_congreso,
                                 u'Nombre del congreso')
                self.assertEqual(data.fecha_de_inicio,
                                 datetime.date(2014, 04, 01))
                self.assertEqual(data.fecha_de_fin,
                                 datetime.date(2014, 04, 05))
                self.assertEqual(data.ciudad_de_realizacion,
                                 u'Ciudad de realización')
                self.assertEqual(data.autores, u'STIC')
                self.assertEqual(data.ambito, u'Autonómica')

    def test_check_read_data_publication(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        u = UserFactory.create()
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
            tipo = parse_produccion_type(item)
            if tipo == 'Publicacion':
                data = Publicacion.objects.create(item, u.profile)
                if data.tipo_de_produccion == 'Articulo':
                    self.assertEqual(data.titulo, u'TÍTULO')
                    self.assertEqual(data.nombre_publicacion, u'NOMBRE')
                    self.assertEqual(data.autores, u'STIC; STIC2')
                else:
                    self.assertEqual(data.titulo, u'Título de la publicación')
                    self.assertEqual(data.nombre_publicacion,
                                     u'Nombre de la publicación')
                    if data.tipo_de_produccion == 'Libro':
                        self.assertEqual(data.autores, u'STIC')
                    else:
                        self.assertEqual(data.autores, u'Firma')
                self.assertEqual(data.volumen, u'1')
                self.assertEqual(data.numero, u'1')
                self.assertEqual(data.pagina_inicial, u'1')
                self.assertEqual(data.pagina_final, u'100')
                self.assertEqual(data.fecha, datetime.date(2014, 04, 01))
                if data.tipo_de_produccion != 'Libro':
                    self.assertEqual(data.issn, u'0395-2037')

    def test_check_read_data_project(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        u = UserFactory.create()
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
            tipo = parse_produccion_type(item)
            if tipo == 'Proyecto' or tipo == 'Convenio':
                data = {}
                if tipo == 'Proyecto':
                    data = Proyecto.objects.create(item, u.profile)
                elif tipo == 'Convenio':
                    data = Convenio.objects.create(item, u.profile)
                self.assertEqual(data.denominacion_del_proyecto,
                                 u'Denominación del proyecto')
                self.assertEqual(data.fecha_de_inicio,
                                 datetime.date(2014, 04, 01))
                if tipo == 'Proyecto':
                    self.assertEqual(data.fecha_de_fin,
                                     datetime.date(2015, 05, 02))
                else:
                    self.assertEqual(data.duracion, 396)
                if tipo == 'Proyecto':
                    self.assertEqual(data.autores, u'Firma')
                    self.assertEqual(data.ambito, u'Internacional no UE')
                else:
                    self.assertEqual(data.autores, u'STIC')
                    self.assertEqual(data.ambito, u'Autonómica')
                self.assertEqual(data.cod_segun_financiadora,
                                 u'Cód. según financiadora')
                self.assertEqual(data.cuantia_total, 1)
                self.assertEqual(data.cuantia_subproyecto, 1)
                self.assertEqual(data.porcentaje_en_subvencion, 1)
                self.assertEqual(data.porcentaje_en_credito, 1)
                self.assertEqual(data.porcentaje_mixto, 1)

    def test_check_read_data_tesis(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        u = UserFactory.create()
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
            data = {}
            tipo = parse_produccion_type(item)
            if tipo == 'TesisDoctoral':
                data = TesisDoctoral.objects.create(item, u.profile)
                self.assertEqual(data.titulo, u'Título del trabajo')
                self.assertEqual(data.universidad_que_titula,
                                 u'Universidad que titula')
                self.assertEqual(data.autor, u'Firma')
                self.assertEqual(data.codirector, u'Firma')
                self.assertEqual(data.fecha_de_lectura,
                                 datetime.date(2014, 04, 01))

    def test_on_insert_cvn_old_pdf_is_moved(self):
        u = UserFactory.create()
        cvn = UploadCVNForm.CVN(u, os.path.join(
            stCVN.TEST_ROOT, 'cvn/CVN-ULL.pdf'))
        relative_path = (
            cvn.cvn_file.name.split('/')[-1].split('.')[0] + '-' +
            cvn.updated_at.strftime('%Y-%m-%d') + '.pdf')
        full_path = os.path.join(stCVN.OLD_PDF_ROOT, relative_path)
        cvn = UploadCVNForm.CVN(u, os.path.join(
            stCVN.TEST_ROOT, 'cvn/CVN-ULL.pdf'))
        self.assertTrue(os.path.isfile(full_path))

    def test_check_change_date_cvn(self):
        date_1 = datetime.date(2014, 4, 3)
        date_2 = datetime.date(2013, 3, 3)
        date_3 = datetime.date(2014, 4, 3)
        date_4 = datetime.date(2002, 3, 2)
        duration_1 = 60
        duration_2 = 136
        p = Proyecto(fecha_de_inicio=date_1,
                     fecha_de_fin=date_2)
        p.save()
        p.fecha_de_fin = date_3
        p.save()
        c = Convenio(fecha_de_inicio=date_4,
                     duracion=duration_1)
        c.save()
        c.duracion = duration_2
        c.save()
        p_duration = date_3 - date_1
        c_date = date_4 + datetime.timedelta(days=duration_2)
        self.assertEqual(p.duracion, p_duration.days)
        self.assertEqual(c.fecha_de_fin, c_date)

    def test_valid_identity_nif_without_letter(self):
        user = UserFactory.create()
        user.profile.documento = '00000000A'
        user.profile.save()
        cvn = UploadCVNForm.CVN(user, os.path.join(
            stCVN.TEST_ROOT, 'cvn/CVN-NIF-sin_letra.pdf'))
        self.assertNotEqual(cvn.status, stCVN.CVNStatus.INVALID_IDENTITY)
