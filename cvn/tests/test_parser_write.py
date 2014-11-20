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

class ParserWriterTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        init()

    def test_parse_cargos(self):
        user = UserFactory.create()
        parser = CvnXmlWriter(user)
        f = open(os.path.join(st_cvn.TEST_ROOT,'csv/cargos.csv'))
        reader = csv.DictReader(f, delimiter='|')
        for row in reader:
            del(row['NIF'])
            del(row['ANYO'])
            del(row['APELLIDO1'])
            del(row['APELLIDO2'])
            del(row['NOMBRE'])
            del(row['COD_FAMILIA_CARGO'])
            del(row['DES1_FAMILIA_CARGO'])
            del(row['COD_CARGO'])
            del(row['F_NOMBRAMIENTO'])
            del(row['COD_DEPARTAMENTO'])
            del(row['COD_DEDICACION'])
            del(row['COD_PERSONA'])
            row['full_time'] = (row['full_time'] == 'Tiempo Completo')
            try:
                row['end_date'] = datetime.datetime.strptime(row['end_date'],
                                                             '%d/%m/%Y').date()
            except ValueError:
                del(row['end_date'])
            row['start_date'] = datetime.datetime.strptime(row['start_date'],
                                                         '%d/%m/%Y').date()
            row['employer'] = 'Universidad de La Laguna'
            parser.add_profession(**row)
        cvn = CVN.create(user, parser.tostring())
        self.assertNotEqual(cvn, None)

    @classmethod
    def tearDownClass(cls):
        clean()