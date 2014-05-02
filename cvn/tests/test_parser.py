# -*- encoding: UTF-8 -*-

from django.test import TestCase
import os
from cvn.parser_helpers import parse_date, parse_date_interval
from cvn import settings as stCVN
from lxml import etree
import datetime


class ParserTestCase(TestCase):

    def setUp(self):
        self.xml_dates = open(os.path.join(stCVN.TEST_ROOT,
                              'xml/dates.xml'), 'r')

    def test_parse_dates(self):
        dates = etree.parse(self.xml_dates).findall('Date')
        self.xml_dates.seek(0)
        for date in dates:
            date_id = int(date.find('date_id').text)

            # OnlyDate
            if date_id == 1:
                parsed_date = parse_date(date)
                self.assertEqual(parsed_date, datetime.date(2014, 03, 02))

            # StartDate, EndDate (2016), duration (2012)
            if date_id == 2:
                #parsed_date = parse_date(date)
                #parsed_end_date = parse_end_date(date)
                (parsed_date, parsed_end_date,
                 parsed_duration) = parse_date_interval(date)
                self.assertEqual(parsed_date, datetime.date(2011, 05, 01))
                self.assertEqual(parsed_end_date, datetime.date(2016, 01, 01))

            # StartDate, Duration
            if date_id == 3:
                parsed_date = parse_date(date)
                self.assertEqual(parsed_date, datetime.date(2010, 07, 04))

            # StartDate, EndDate (2006), duration (2013)
            if date_id == 4:
                #parsed_date = parse_date(date)
                #parsed_end_date = parse_end_date(date)
                (parsed_date, parsed_end_date,
                    parsed_duration) = parse_date_interval(date)
                self.assertEqual(parsed_date, datetime.date(2012, 05, 01))
                self.assertEqual(parsed_end_date, datetime.date(2013, 06, 02))

            # Date > item
            if date_id == 5:
                parsed_date = parse_date(date)
                self.assertEqual(parsed_date, datetime.date(2001, 01, 02))
