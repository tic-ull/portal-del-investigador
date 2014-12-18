# -*- encoding: UTF-8 -*-

import os

from django.test import TestCase

from cvn import settings as st_cvn
from cvn.models import CVN, OldCvnPdf
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

    def test_on_insert_cvn_old_pdf_is_moved(self):
        us = UserFactory.create()
        cvn = CVN(user=us, pdf_path=os.path.join(
            st_cvn.TEST_ROOT, 'cvn/CVN-Test.pdf'))
        cvn.save()
        CVN(user=us, pdf_path=os.path.join(
            st_cvn.TEST_ROOT, 'cvn/CVN-Test.pdf'))
        self.assertIsNotNone(OldCvnPdf.objects.get(user_profile=us.profile))

    def test_valid_identity_nif_without_letter(self):
        user = UserFactory.create()
        user.profile.documento = '11111111H'
        user.profile.save()
        cvn = CVN(user=user, pdf_path=os.path.join(
            st_cvn.TEST_ROOT, 'cvn/CVN-NIF-sin_letra.pdf'))
        self.assertNotEqual(cvn.status, st_cvn.CVNStatus.INVALID_IDENTITY)

    def test_update_from_pdf(self):
        us = UserFactory.create()
        cvn = CVN(user=us)
        pdf_file = file(os.path.join(st_cvn.TEST_ROOT, 'cvn/CVN-Test.pdf'))
        cvn.update_from_pdf(pdf_file.read())
        self.assertTrue(cvn.xml_file and cvn.cvn_file)

    def test_update_from_xml(self):
        us = UserFactory.create()
        cvn = CVN(user=us)
        xml_file = file(os.path.join(st_cvn.TEST_ROOT, 'xml/CVN-Test.xml'))
        cvn.update_from_xml(xml_file.read())
        self.assertTrue(cvn.xml_file and cvn.cvn_file)

    @classmethod
    def tearDownClass(cls):
        clean()
