# -*- encoding: UTF-8 -*-

from django.conf import settings as st


def external_urls(request):
    return {'old_portal': st.OLD_PORTAL_URL}
