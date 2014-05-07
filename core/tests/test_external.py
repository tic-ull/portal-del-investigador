# -*- encoding: UTF-8 -*-

from django.test import TestCase
from django.conf import settings as st
import urllib


class ExternalTests(TestCase):

    def test_ws_is_alive(self):
        WS = st.WS_SERVER_URL + 'get_codpersona?nif=.'
        self.assertEqual(urllib.urlopen(WS).code, 200)
