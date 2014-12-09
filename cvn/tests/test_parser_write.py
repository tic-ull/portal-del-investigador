# -*- encoding: UTF-8 -*-

from core.tests.factories import UserFactory
from core.tests.helpers import init, clean
from cvn import settings as st_cvn
from cvn.models import CVN
from cvn.parsers.read import parse_cvnitem
from cvn.parsers.write import CvnXmlWriter
from django.test import TestCase
from factories import (LearningPhdFactory, ProfessionFactory)
from lxml import etree

import csv
import datetime
import os


class ParserWriterTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        init()

    @staticmethod
    def utf_8_encoder(unicode_csv_data):
        for line in unicode_csv_data:
            yield line.decode('iso-8859-10').encode('utf-8')

    def test_cvnitem_factories(self):
        user = UserFactory.create()
        parser = CvnXmlWriter(user)
        cvnitem_dict = {}
        # Insert old and new professions in the CVN
        for i in range(0, 10):
            d = ProfessionFactory.create()
            cvnitem_dict[d['title']] = d
            parser.add_profession(**d)
        # Insert Phd the researcher has received
        for i in range(0, 10):
            d = LearningPhdFactory.create()
            cvnitem_dict[d['title']] = d
            parser.add_learning_phd(**d)

        cvn = CVN.create(user, parser.tostring())
        cvn.xml_file.open()
        cvn_items = etree.parse(cvn.xml_file).findall('CvnItem')
        for item in cvn_items:
            cvnitem = parse_cvnitem(item)
            self.assertEqual(cmp(cvnitem, cvnitem_dict[cvnitem['title']]), 0)
        self.assertNotEqual(cvn, None)

    def test_parse_cargos(self):
        user = UserFactory.create()
        parser = CvnXmlWriter(user)
        f = open(os.path.join(st_cvn.TEST_ROOT, 'csv/cargos.csv'))
        reader = csv.DictReader(self.utf_8_encoder(f), delimiter='|')
        now = datetime.datetime.now().date()
        for row in reader:
            # Remove what identifies the user
            del(row['NIF'])
            # Transform full time to boolean
            # We expect it to be boolean in the ws
            row['full_time'] = (row['full_time'] == 'Tiempo Completo')
            # Transform the dates into datetime.date objects. We expect them
            # to be datetime.date objects in the ws.
            try:
                end_date = datetime.datetime.strptime(
                    row['end_date'], '%d/%m/%Y').date()
                if end_date < now:
                    row['end_date'] = end_date
                else:
                    del(row['end_date'])
            except ValueError:
                del(row['end_date'])
            row['start_date'] = datetime.datetime.strptime(
                row['start_date'], '%d/%m/%Y').date()
            # We add the employer. It is not sent because it always is
            # Universidad de La Laguna
            row['employer'] = 'Universidad de La Laguna'
            parser.add_profession(**row)
        cvn = CVN.create(user, parser.tostring())
        self.assertNotEqual(cvn, None)

    def test_parse_categorias(self):
        user = UserFactory.create()
        parser = CvnXmlWriter(user)
        f = open(os.path.join(st_cvn.TEST_ROOT, 'csv/categorias.csv'))
        reader = csv.DictReader(self.utf_8_encoder(f), delimiter='|')
        now = datetime.datetime.now().date()
        for row in reader:
            # Remove what identifies the user
            del(row['NIF'])
            # Transform full time to boolean
            # We expect it to be boolean in the ws
            row['full_time'] = (row['full_time'].upper()
                                == 'Tiempo Completo'.upper())
            # Transform the dates into datetime.date objects. We expect them
            # to be datetime.date objects in the ws.
            try:
                end_date = datetime.datetime.strptime(
                    row['end_date'], '%d/%m/%y').date()
                if end_date < now:
                    row['end_date'] = end_date
                else:
                    del(row['end_date'])
            except ValueError:
                del(row['end_date'])
            row['start_date'] = datetime.datetime.strptime(
                row['start_date'], '%d/%m/%y').date()
            # We add the employer. It is not sent because it always is
            # Universidad de La Laguna
            row['employer'] = 'Universidad de La Laguna'
            parser.add_profession(**row)
        cvn = CVN.create(user, parser.tostring())
        self.assertNotEqual(cvn, None)

    @classmethod
    def tearDownClass(cls):
        clean()
