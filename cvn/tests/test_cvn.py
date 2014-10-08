# -*- encoding: UTF-8 -*-

from cvn import settings as st_cvn
from cvn.models import (CVN, Congreso, Convenio, Proyecto,
                        TesisDoctoral, Articulo, Libro, Capitulo)
from cvn.parser_helpers import parse_produccion_type, parse_produccion_subtype
from core.tests.helpers import init, clean
from django.test import TestCase
from core.tests.factories import UserFactory
from lxml import etree
from cvn.forms import UploadCVNForm
import datetime
import os


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

    def test_on_insert_cvn_old_pdf_is_moved(self):
        u = UserFactory.create()
        cvn = UploadCVNForm.CVN(u, os.path.join(
            st_cvn.TEST_ROOT, 'cvn/CVN-Test.pdf'))
        relative_path = (
            cvn.cvn_file.name.split('/')[-1].split('.')[0] + '-' +
            cvn.updated_at.strftime('%Y-%m-%d') + '.pdf')
        full_path = os.path.join(st_cvn.OLD_PDF_ROOT, relative_path)
        UploadCVNForm.CVN(u, os.path.join(
            st_cvn.TEST_ROOT, 'cvn/CVN-Test.pdf'))
        self.assertTrue(os.path.isfile(full_path))

    def test_valid_identity_nif_without_letter(self):
        user = UserFactory.create()
        user.profile.documento = '11111111H'
        user.profile.save()
        cvn = UploadCVNForm.CVN(user, os.path.join(
            st_cvn.TEST_ROOT, 'cvn/CVN-NIF-sin_letra.pdf'))
        self.assertNotEqual(cvn.status, st_cvn.CVNStatus.INVALID_IDENTITY)

    @classmethod
    def tearDownClass(cls):
        clean()
