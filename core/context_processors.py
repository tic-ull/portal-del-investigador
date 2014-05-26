# -*- encoding: UTF-8 -*-

from django.conf import settings as st


def extra_info(request):
    return {
        'old_portal': st.OLD_PORTAL_URL,
    }
