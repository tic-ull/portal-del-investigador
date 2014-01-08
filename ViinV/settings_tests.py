# -*- encoding: utf-8 -*-
from django.conf import settings as st
import os

ID_TEST = 99999

CVN_LOCATION = os.path.join(st.PROJECT_ROOT, 'cvn/tests/CVN-invbecario.pdf')
CVN_NOT_FECYT_LOCATION = os.path.join(st.PROJECT_ROOT,
                                      'cvn/tests/CVN-invbecario-notFecyt.pdf')
CVN_FILE = os.path.join(st.MEDIA_ROOT, 'cvn/pdf/CVN-test-709bddb1.pdf')
XML_FILE = os.path.join(st.MEDIA_ROOT, 'cvn/xml/CVN-test-709bddb1.xml')

USER_LOGIN = "invbecario"
USER_PASSWD = "pruebasINV1"
USER_NIF = "123456789A"

ADMIN_LOGIN = "admin"
ADMIN_PASSWD = "123"

