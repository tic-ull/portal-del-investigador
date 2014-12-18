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
        relative_path = (
            'old/' + cvn.cvn_file.name.split('/')[-1].split('.')[0] + '-' +
            cvn.uploaded_at.strftime('%Y-%m-%d-%Hh%Mm%Ss') + '.pdf')
        root_dir = '/'.join(cvn.cvn_file.path.split('/')[:-1])
        full_path = os.path.join(root_dir, relative_path)
        CVN(user=us, pdf_path=os.path.join(
            st_cvn.TEST_ROOT, 'cvn/CVN-Test.pdf'))
        self.assertTrue(os.path.isfile(full_path))
        self.assertIsNotNone(
            OldCvnPdf.objects.get(user_profile=us.profile,
                                  uploaded_at=cvn.uploaded_at))

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
