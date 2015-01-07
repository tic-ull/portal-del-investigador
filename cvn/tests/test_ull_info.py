# -*- encoding: UTF-8 -*-

import os

from django.test import TestCase

from cvn import settings as st_cvn
from core.tests.helpers import init, clean
from core.tests.factories import UserFactory
from mock import patch
from core.ws_utils import CachedWS
from cvn.models import CVN
from django.conf import settings as st
from cvn.parsers.read import parse_cvnitem
from cvn.helpers import DateRange
import datetime
from lxml import etree


@classmethod
def get_all(cls, url, use_redis=True, timeout=None):
    if url == st.WS_ULL_LEARNING % 'example_code':
        return [{u'des1_titulacion': u'LICENCIADO EN MATEMATICAS',
                 u'organismo': u'UNIVERSIDAD DE LA LAGUNA',
                 u'f_expedicion': u'18-12-2001',
                 u'des1_grado_titulacion': u'Licenciado/Ingeniero Superior'},
                {u'des1_titulacion': u'Doctor por la Universidad de La Laguna',
                 u'organismo': u'UNIVERSIDAD DE LA LAGUNA',
                 u'f_expedicion': u'07-07-2006',
                 u'des1_grado_titulacion': u'Doctor'}]
    elif url == st.WS_ULL_CARGOS % 'example_code':
        return [{u'dedicacion': u'Tiempo Completo',
                 u'des1_cargo': u'SECRETARIO DPTO ANALISIS MATEMATICO',
                 u'centro': u'DPTO.ANALISIS MATEMATICO',
                 u'departamento': u'AN\xc1LISIS MATEM\xc1TICO',
                 u'f_hasta': u'13-02-2013', u'f_toma_posesion': u'30-11-2010'}]


@classmethod
def get_learning(cls, url, use_redis=True, timeout=None):
    if url == st.WS_ULL_LEARNING % 'example_code':
        return [{u'des1_titulacion': u'LICENCIADO EN MATEMATICAS',
                 u'organismo': u'UNIVERSIDAD DE LA LAGUNA',
                 u'f_expedicion': u'18-12-2001',
                 u'des1_grado_titulacion': u'Licenciado/Ingeniero Superior'},
                {u'des1_titulacion': u'Doctor por la Universidad de La Laguna',
                 u'organismo': u'UNIVERSIDAD DE LA LAGUNA',
                 u'f_expedicion': u'07-07-2006',
                 u'des1_grado_titulacion': u'Doctor'}]
    else:
        return []


@classmethod
def get_cargos(cls, url, use_redis=True, timeout=None):
    if url == st.WS_ULL_CARGOS % 'example_code':
        return [{u'dedicacion': u'Tiempo Completo',
                 u'des1_cargo': u'SECRETARIO DPTO ANALISIS MATEMATICO',
                 u'centro': u'DPTO.ANALISIS MATEMATICO',
                 u'departamento': u'AN\xc1LISIS MATEM\xc1TICO',
                 u'f_hasta': u'13-02-2013', u'f_toma_posesion': u'30-11-2010'}]
    else:
        return []


class UllInfoTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        init()

    def setUp(self):
        self.xml_ull = open(os.path.join(st_cvn.FILE_TEST_ROOT,
                            'xml/CVN-ULL.xml'))
        self.xml_empty = open(os.path.join(st_cvn.FILE_TEST_ROOT,
                              'xml/empty.xml'))
        self.xml_test = open(os.path.join(st_cvn.FILE_TEST_ROOT,
                             'xml/CVN-Test.xml'))

    @patch.object(CachedWS, 'get', get_learning)
    def test_get_pdf_ull_learning(self):
        user = UserFactory.create()
        user.profile.rrhh_code = 'example_code'
        pdf = CVN.get_user_pdf_ull(user=user)
        cvn = CVN(user=user, pdf=pdf)
        cvn.xml_file.open()
        cvn_items = etree.parse(cvn.xml_file).findall('CvnItem')
        ws_content = CachedWS.get(st.WS_ULL_LEARNING % 'example_code')
        for w in ws_content:
            CVN._learning_to_json(w)
            if 'title_type' in w:
                w['title_type'] = w['title_type'].upper()

        pdf_content = []
        for item in cvn_items:
            pdf_content.append(parse_cvnitem(item))

        self.assertEqual(len(ws_content), len(pdf_content))
        allequal = True
        for wi in ws_content:
            equal = False
            for pi in pdf_content:
                if cmp(wi, pi) == 0:
                    equal = True
            if not equal:
                allequal = False
        self.assertTrue(allequal)

    @patch.object(CachedWS, 'get', get_cargos)
    def test_get_pdf_ull_cargos(self):
        user = UserFactory.create()
        user.profile.rrhh_code = 'example_code'
        pdf = CVN.get_user_pdf_ull(user=user)
        cvn = CVN(user=user, pdf=pdf)
        cvn.xml_file.open()
        cvn_items = etree.parse(cvn.xml_file).findall('CvnItem')
        ws_content = CachedWS.get(st.WS_ULL_CARGOS % 'example_code')
        for w in ws_content:
            CVN._cargo_to_json(w)
            if not 'employer' in w:
                w['employer'] = 'Universidad de La Laguna'

        pdf_content = []
        for item in cvn_items:
            pdf_content.append(parse_cvnitem(item))

        self.assertEqual(len(ws_content), len(pdf_content))
        allequal = True
        for wi in ws_content:
            equal = False
            for pi in pdf_content:
                if cmp(wi, pi) == 0:
                    equal = True
            if not equal:
                allequal = False
        self.assertTrue(allequal)

    @patch.object(CachedWS, 'get', get_all)
    def test_get_pdf_ull_filter_by_date(self):
        user = UserFactory.create()
        user.profile.rrhh_code = 'example_code'
        pdf = CVN.get_user_pdf_ull(user=user)
        cvn = CVN(user=user, pdf=pdf)
        cvn.xml_file.open()
        self.assertEqual(len(etree.parse(cvn.xml_file).findall('CvnItem')), 3)

        pdf = CVN.get_user_pdf_ull(user=user)
        cvn = CVN(user=user, pdf=pdf)
        cvn.xml_file.open()
        self.assertEqual(len(etree.parse(cvn.xml_file).findall('CvnItem')), 3)

        pdf = CVN.get_user_pdf_ull(user=user, start_date=datetime.date(2012, 1, 1))
        cvn = CVN(user=user, pdf=pdf)
        cvn.xml_file.open()
        self.assertEqual(len(etree.parse(cvn.xml_file).findall('CvnItem')), 1)

        pdf = CVN.get_user_pdf_ull(user=user, end_date=datetime.date(2010, 1, 1))
        cvn = CVN(user=user, pdf=pdf)
        cvn.xml_file.open()
        self.assertEqual(len(etree.parse(cvn.xml_file).findall('CvnItem')), 2)

        pdf = CVN.get_user_pdf_ull(user=user, start_date=datetime.date(2006, 1, 1),
                              end_date=datetime.date(2011, 1, 1))
        cvn = CVN(user=user, pdf=pdf)
        cvn.xml_file.open()
        self.assertEqual(len(etree.parse(cvn.xml_file).findall('CvnItem')), 2)

    def test_ws_ull_learning(self):
        ws_info = CachedWS.get(st.WS_ULL_LEARNING % 29739)
        with patch.object(CachedWS, 'get', get_learning):
            test_info = CachedWS.get(st.WS_ULL_LEARNING % 'example_code')
        self.assertEqual(ws_info, test_info)

    def test_ws_ull_cargos(self):
        ws_info = CachedWS.get(st.WS_ULL_CARGOS % 29739)
        with patch.object(CachedWS, 'get', get_cargos):
            test_info = CachedWS.get(st.WS_ULL_CARGOS % 'example_code')
        self.assertEqual(ws_info, test_info)

    def test_daterange(self):
        date1 = datetime.date(2001, 1, 1)
        date2 = datetime.date(2001, 12, 31)
        date3 = datetime.date(2002, 1, 1)
        date4 = datetime.date(2003, 1, 1)
        range1 = DateRange(date1, date2)
        range2 = DateRange(date3, date4)
        range3 = DateRange(date2, date4)
        range4 = DateRange(date1, date1)
        range5 = DateRange(date3, date3)
        range6 = DateRange(None, date3)
        range7 = DateRange(date2, None)
        range8 = DateRange(date4, date4)
        range9 = DateRange(date1, date3)
        range10 = DateRange(date2, date4)
        self.assertFalse(range1.intersect(range2))
        self.assertFalse(range3.intersect(range4))
        self.assertTrue(range3.intersect(range5))
        self.assertTrue(range6.intersect(range1))
        self.assertFalse(range6.intersect(range8))
        self.assertTrue(range7.intersect(range8))
        self.assertFalse(range7.intersect(range4))
        self.assertTrue(range9.intersect(range10))

    @classmethod
    def tearDownClass(cls):
        clean()