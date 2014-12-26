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
from lxml import etree


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
        self.xml_ull = open(os.path.join(st_cvn.TEST_ROOT,
                            'xml/CVN-ULL.xml'))
        self.xml_empty = open(os.path.join(st_cvn.TEST_ROOT,
                              'xml/empty.xml'))
        self.xml_test = open(os.path.join(st_cvn.TEST_ROOT,
                             'xml/CVN-Test.xml'))

    @patch.object(CachedWS, 'get', get_learning)
    def test_get_pdf_ull_learning(self):
        user = UserFactory.create()
        user.profile.rrhh_code = 'example_code'
        pdf = CVN.get_pdf_ull(user=user)
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
        pdf = CVN.get_pdf_ull(user=user)
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

    def test_ws_ull_learning(self):
        rrhh_code = 29739

    def test_ws_ull_cargos(self):
        rrhh_code = 29739

    @classmethod
    def tearDownClass(cls):
        clean()