# -*- encoding: UTF-8 -*-

from django.test import TestCase
from django.conf import settings as st
import urllib


class ExternalTests(TestCase):

    def test_ws_is_alive(self):
        self.assertEqual(urllib.urlopen(st.WS_COD_PERSONA % '.').code, 200)
