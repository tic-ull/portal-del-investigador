# -*- encoding: UTF-8 -*-

from cvn import settings as st_cvn
from cvn.parsers.read import (parse_date, parse_date_interval,
                              parse_produccion_id, parse_places)
from django.test import TestCase
from lxml import etree

import datetime
import os


class ParserTestCase(TestCase):

    def test_parse_dates(self):
        xml_dates = open(os.path.join(st_cvn.FILE_TEST_ROOT, 'xml/dates.xml'))
        dates = etree.parse(xml_dates).findall('Date')
        for date in dates:
            date_id = int(date.find('date_id').text)

            # OnlyDate (DayMonthYear)
            if date_id == 1:
                parsed_date = parse_date(date)
                self.assertEqual(parsed_date, datetime.date(2014, 03, 02))

            # StartDate (MonthYear), EndDate (Year: 2016), duration (2012)
            if date_id == 2:
                (parsed_date, parsed_end_date,
                 parsed_duration) = parse_date_interval(date)
                self.assertEqual(parsed_date, datetime.date(2011, 05, 01))
                self.assertEqual(parsed_end_date, datetime.date(2016, 01, 01))
                duration = parsed_end_date - parsed_date
                self.assertEqual(parsed_duration, duration.days)

            # StartDate (DayMonthYear), Duration
            if date_id == 3:
                parsed_date = parse_date(date)
                self.assertEqual(parsed_date, datetime.date(2010, 07, 04))

            # StartDate (MonthYear), EndDate (Year: 2006), duration (2013)
            if date_id == 4:
                (parsed_date, parsed_end_date,
                    parsed_duration) = parse_date_interval(date)
                self.assertEqual(parsed_date, datetime.date(2012, 05, 01))
                self.assertEqual(parsed_end_date, datetime.date(2013, 06, 01))
                duration = parsed_end_date - parsed_date
                self.assertEqual(parsed_duration, duration.days)

            # Date > item
            if date_id == 5:
                parsed_date = parse_date(date)
                self.assertEqual(parsed_date, datetime.date(2001, 01, 02))

            # All None
            if date_id == 6:
                (parsed_date, parsed_end_date,
                    parsed_duration) = parse_date_interval(date)
                self.assertEqual(parsed_date, None)
                self.assertEqual(parsed_end_date, None)
                self.assertEqual(parsed_duration, None)

            # StartDate (DayMonthYear), EndDate (Year)
            if date_id == 7:
                (parsed_date, parsed_end_date,
                    parsed_duration) = parse_date_interval(date)
                self.assertEqual(parsed_date, datetime.date(2009, 01, 02))
                self.assertEqual(parsed_end_date, datetime.date(2010, 01, 01))
                duration = parsed_end_date - parsed_date
                self.assertEqual(parsed_duration, duration.days)

            # EndDate, Duration (duration is useless here)
            if date_id == 8:
                (parsed_date, parsed_end_date,
                    parsed_duration) = parse_date_interval(date)
                self.assertEqual(parsed_date, None)
                self.assertEqual(parsed_end_date, datetime.date(1997, 07, 04))
                self.assertEqual(parsed_duration, None)

            # Duration (duration is useless here)
            if date_id == 9:
                (parsed_date, parsed_end_date,
                    parsed_duration) = parse_date_interval(date)
                self.assertEqual(parsed_date, None)
                self.assertEqual(parsed_end_date, None)
                self.assertEqual(parsed_duration, None)

    def test_parse_publicacion_ids(self):
        xml_externalpks = open(os.path.join(st_cvn.FILE_TEST_ROOT,
                                            'xml/externalpks.xml'))
        ids = etree.parse(xml_externalpks).findall('ExternalPK')
        pids = parse_produccion_id(ids)
        issn = pids[st_cvn.PRODUCTION_ID_CODE['ISSN']]
        isbn = pids[st_cvn.PRODUCTION_ID_CODE['ISBN']]
        financiadora = pids[st_cvn.PRODUCTION_ID_CODE['FINANCIADORA']]
        deposito_legal = pids[st_cvn.PRODUCTION_ID_CODE['DEPOSITO_LEGAL']]
        self.assertEqual(issn, '0395-2037')
        self.assertEqual(isbn, '1-56619-909-1')
        self.assertEqual(financiadora, 'Cod. segun financiadora')
        self.assertEqual(deposito_legal, 'B-15155-1975')

    def test_parse_place(self):
        xml_patentes = open(os.path.join(
            st_cvn.FILE_TEST_ROOT, 'xml/patentes.xml'))
        patentes = etree.parse(xml_patentes).findall('CvnItem')
        for patente in patentes:
            num_solicitud = patente.find(
                "ExternalPK/Code[@code='050.030.010.110']")
            if (num_solicitud is not None and
                    num_solicitud.find('Item').text == '2'):
                (lugar_prioritario, lugares) = parse_places(
                    patente.findall("Place"))
                self.assertEqual(lugar_prioritario, 'Andorra')
                self.assertEqual(lugares, '')
