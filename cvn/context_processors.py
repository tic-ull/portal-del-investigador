# -*- encoding: UTF-8 -*-

from cvn import settings as st_cvn


def extra_info(request):
    return {
        'EDITOR_FECYT': st_cvn.EDITOR_FECYT,  # URL of FECYT editor
    }
