# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN


def extra_info(request):
    return {
        'EDITOR_FECYT': stCVN.EDITOR_FECYT,  # URL of FECYT editor
    }
