# -*- encoding: UTF-8 -*-

from cvn.parsers.write import CvnXmlWriter
import csv
import os
import cvn.settings as st_cvn
from django.test import TestCase
from core.tests.factories import UserFactory
import datetime
from cvn.models import CVN
from core.tests.helpers import init, clean
from factories import (LearningOtherFactory, LearningPhdFactory,
                       ProfessionFactory, TeachingPhdFactory)

class ParserWriterTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        init()

    @staticmethod
    def utf_8_encoder(unicode_csv_data):
        for line in unicode_csv_data:
            yield line.decode('iso-8859-10').encode('utf-8')

    def test_profession_factory(self):
        user = UserFactory.create()
        parser = CvnXmlWriter(user)
        for i in range(0, 10):
            d = ProfessionFactory.create()
            parser.add_profession(**d)
        cvn = CVN.create(user, parser.tostring())
        self.assertNotEqual(cvn, None)

    def test_teaching_phd_factory(self):
        user = UserFactory.create()
        parser = CvnXmlWriter(user)
        for i in range(0, 10):
            d = TeachingPhdFactory.create()
            parser.add_teaching_phd(**d)
        cvn = CVN.create(user, parser.tostring())
        self.assertNotEqual(cvn, None)

    def test_learning_other_factory(self):
        user = UserFactory.create()
        parser = CvnXmlWriter(user)
        for i in range(0, 10):
            d = LearningOtherFactory.create()
            parser.add_learning_other(**d)
        cvn = CVN.create(user, parser.tostring())
        self.assertNotEqual(cvn, None)

    def test_learning_phd_factory(self):
        user = UserFactory.create()
        parser = CvnXmlWriter(user)
        for i in range(0, 10):
            d = LearningPhdFactory.create()
            parser.add_learning_phd(**d)
        cvn = CVN.create(user, parser.tostring())
        self.assertNotEqual(cvn, None)

    def test_parse_formrecv(self):
        user = UserFactory.create()
        parser = CvnXmlWriter(user)
        f = open(os.path.join(st_cvn.TEST_ROOT,'csv/formacionrecv.csv'))
        reader = csv.DictReader(self.utf_8_encoder(f), delimiter='|')
        now = datetime.datetime.now().date()
        for row in reader:
            # Remove what identifies the user
            del(row['NIF'])
            # Transform the dates into datetime.date objects. We expect them
            # to be datetime.date objects in the ws.
            row['end_date'] = datetime.datetime.strptime(row['end_date'],
                                                         '%Y-%m-%d').date()
            row['start_date'] = datetime.datetime.strptime(row['start_date'],
                                                           '%Y-%m-%d').date()
            parser.add_learning_other(**row)
        cvn = CVN.create(user, parser.tostring())
        self.assertNotEqual(cvn, None)

    def test_parse_cargos(self):
        user = UserFactory.create()
        parser = CvnXmlWriter(user)
        f = open(os.path.join(st_cvn.TEST_ROOT,'csv/cargos.csv'))
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
                end_date = datetime.datetime.strptime(row['end_date'],
                                                             '%d/%m/%Y').date()
                if end_date < now:
                    row['end_date'] = end_date
                else:
                    del(row['end_date'])
            except ValueError:
                del(row['end_date'])
            row['start_date'] = datetime.datetime.strptime(row['start_date'],
                                                         '%d/%m/%Y').date()
            # We add the employer. It is not sent because it always is
            # Universidad de La Laguna
            row['employer'] = 'Universidad de La Laguna'
            parser.add_profession(**row)
        cvn = CVN.create(user, parser.tostring())
        self.assertNotEqual(cvn, None)

    def test_parse_categorias(self):
        user = UserFactory.create()
        parser = CvnXmlWriter(user)
        f = open(os.path.join(st_cvn.TEST_ROOT,'csv/categorias.csv'))
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
                end_date = datetime.datetime.strptime(row['end_date'],
                                                             '%d/%m/%y').date()
                if end_date < now:
                    row['end_date'] = end_date
                else:
                    del(row['end_date'])
            except ValueError:
                del(row['end_date'])
            row['start_date'] = datetime.datetime.strptime(row['start_date'],
                                                         '%d/%m/%y').date()
            # We add the employer. It is not sent because it always is
            # Universidad de La Laguna
            row['employer'] = 'Universidad de La Laguna'
            parser.add_profession(**row)
        cvn = CVN.create(user, parser.tostring())
        self.assertNotEqual(cvn, None)

    @classmethod
    def tearDownClass(cls):
        clean()