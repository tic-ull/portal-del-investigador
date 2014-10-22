# -*- encoding: UTF-8 -*-

from django.conf import settings as st
import os
import shutil


def init():
    st.MEDIA_ROOT = st.MEDIA_TEST_ROOT
    try:
        os.makedirs(st.MEDIA_TEST_ROOT)
    except OSError:
        pass
    if not st.DEBUG:
        st.DEBUG = True


def clean():
    shutil.rmtree(st.MEDIA_TEST_ROOT)
