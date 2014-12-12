# -*- encoding: UTF-8 -*-

import datetime
import os

from django.test import TestCase
from lxml import etree

from cvn import settings as st_cvn
from cvn.models import (CVN, Congreso, Convenio, Proyecto, Patente,
                        TesisDoctoral, Articulo, Libro, Capitulo)
from cvn.parsers.read_helpers import (parse_produccion_type,
                                      parse_produccion_subtype)
from core.tests.helpers import init, clean
from core.tests.factories import UserFactory


class CVNTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        init()

    def setUp(self):
        self.xml_ull = open(os.path.join(st_cvn.TEST_ROOT,
                            'xml/CVN-ULL.xml'))
        self.xml_empty = open(os.path.join(st_cvn.TEST_ROOT,
                              'xml/empty.xml'))
        self.xml_test = open(os.path.join(st_cvn.TEST_ROOT,
                             'xml/CVN-Test.xml'))

    def test_insert_xml_ull(self):
        """ Insert the data of XML in the database """
        try:
            user = UserFactory.create()
            cvn = CVN(user=user, pdf_path=os.path.join(
                st_cvn.TEST_ROOT, 'cvn/CVN-ULL.pdf'))
            cvn.insert_xml()
            self.assertEqual(user.profile.articulo_set.count(), 1074)
            self.assertEqual(user.profile.libro_set.count(), 6)
            self.assertEqual(user.profile.capitulo_set.count(), 32)
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
                count += 1
                Articulo.objects.create(item, u.profile)
        self.assertEqual(count, 1214)
        self.assertEqual(Articulo.objects.all().count(), 1074)

    def test_check_read_data_congress(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        u = UserFactory.create()
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
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
                self.assertEqual(data.autores,
                                 u'Nombre Primer Apellido '
                                 'Segundo Apellido (STIC)')
                self.assertEqual(data.ambito, u'Autonómica')

    def test_check_read_data_publication(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        u = UserFactory.create()
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
            tipo = parse_produccion_type(item)
            subtipo = parse_produccion_subtype(item)
            data = None
            if tipo == 'Publicacion':

                if subtipo == u'Articulo':
                    data = Articulo.objects.create(item, u.profile)
                    self.assertEqual(data.titulo, u'TÍTULO')
                    self.assertEqual(data.nombre_publicacion, u'NOMBRE')
                    self.assertEqual(data.autores,
                                     u'NOMBRE APELLIDO1 APELLIDO2 (STIC); '
                                     'NOMBRE2 APELLIDO12 APELLIDO22 (STIC2)')
                    self.assertEqual(data.issn, u'0395-2037')

                if subtipo == u'Libro':
                    data = Libro.objects.create(item, u.profile)
                    self.assertEqual(data.titulo, u'Título de la publicación')
                    self.assertEqual(data.nombre_publicacion,
                                     u'Nombre de la publicación')
                    self.assertEqual(data.autores,
                                     u'Nombre Primer Apellido '
                                     'Segundo Apellido (STIC)')

                if subtipo == u'Capitulo':
                    data = Capitulo.objects.create(item, u.profile)
                    self.assertEqual(data.titulo, u'Título de la publicación')
                    self.assertEqual(data.nombre_publicacion,
                                     u'Nombre de la publicación')
                    self.assertEqual(data.autores,
                                     u'Nombre Primer Apellido '
                                     'Segundo Apellido (Firma)')
                    self.assertEqual(data.issn, u'0395-2037')

                self.assertEqual(data.volumen, u'1')
                self.assertEqual(data.numero, u'1')
                self.assertEqual(data.pagina_inicial, u'1')
                self.assertEqual(data.pagina_final, u'100')
                self.assertEqual(data.fecha, datetime.date(2014, 04, 01))

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
                self.assertEqual(data.titulo,
                                 u'Denominación del proyecto')
                self.assertEqual(data.fecha_de_inicio,
                                 datetime.date(2014, 04, 01))
                if tipo == 'Proyecto':
                    self.assertEqual(data.fecha_de_fin,
                                     datetime.date(2015, 05, 02))
                else:
                    self.assertEqual(data.duracion, 396)
                if tipo == 'Proyecto':
                    self.assertEqual(data.autores,
                                     u'Nombre Primer Apellido '
                                     'Segundo Apellido (Firma)')
                    self.assertEqual(data.ambito, u'Internacional no UE')
                else:
                    self.assertEqual(data.autores,
                                     u'Nombre Primer Apellido '
                                     'Segundo Apellido (STIC)')
                    self.assertEqual(data.ambito, u'Autonómica')
                self.assertEqual(data.cod_segun_financiadora,
                                 u'Cód. según financiadora')
                self.assertEqual(data.cuantia_total, '1')
                self.assertEqual(data.cuantia_subproyecto, '1')
                self.assertEqual(data.porcentaje_en_subvencion, '1')
                self.assertEqual(data.porcentaje_en_credito, '1')
                self.assertEqual(data.porcentaje_mixto, '1')

    def test_check_read_data_tesis(self):
        cvn = CVN(xml_file=self.xml_test)
        cvn.xml_file.seek(0)
        u = UserFactory.create()
        items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in items:
            tipo = parse_produccion_type(item)
            if tipo == 'TesisDoctoral':
                data = TesisDoctoral.objects.create(item, u.profile)
                self.assertEqual(data.titulo, u'Título del trabajo')
                self.assertEqual(data.universidad_que_titula,
                                 u'Universidad que titula')
                self.assertEqual(data.autor,
                                 u'Nombre Primer Apellido '
                                 'Segundo Apellido (Firma)')
                self.assertEqual(data.codirector,
                                 u'Nombre Primer Apellido '
                                 'Segundo Apellido (Firma)')
                self.assertEqual(data.fecha,
                                 datetime.date(2014, 04, 01))

    def test_productions_no_title(self):
        u = UserFactory.create()
        cvn = CVN(user=u, pdf_path=os.path.join(
            st_cvn.TEST_ROOT, 'cvn/produccion_sin_titulo.pdf'))
        cvn.insert_xml()
        self.assertEqual(len(u.profile.proyecto_set.all()), 3)
        self.assertEqual(len(Articulo.objects.filter(user_profile__user=u)), 3)

    def test_insert_patentes(self):
        u = UserFactory.create()
        cvn = CVN(user=u, pdf_path=os.path.join(
            st_cvn.TEST_ROOT, 'cvn/cvn-patentes.pdf'))
        cvn.insert_xml()
        patente = Patente.objects.get(num_solicitud=111111111111111)
        self.assertEqual(patente.titulo, "Patente uno")
        self.assertEqual(patente.fecha, datetime.date(2011, 01, 01))
        self.assertEqual(patente.fecha_concesion, datetime.date(2011, 01, 02))
        self.assertEqual(patente.lugar_prioritario, u'Canarias, Spain')
        self.assertEqual(patente.lugares, u'Israel; Andalucía, Spain')
        self.assertEqual(patente.autores,
                         u'Judas Iscariote (JI); Juan Rodríguez González')
        self.assertEqual(patente.entidad_titular,
                         u'BANCO POPULAR ESPAÑOL, S.A.')
        self.assertEqual(patente.empresas,
                         u'Banco Pastor; CEMUSA CORPORACION EUROPEA DE '
                         'MOBILIARIO URBANO SA')

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

    @classmethod
    def tearDownClass(cls):
        clean()
