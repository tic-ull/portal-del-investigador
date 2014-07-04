# -*- encoding: UTF-8 -*-

import settings as stCVN


def extra_info(request):
    return {
        'EDITOR_FECYT': stCVN.EDITOR_FECYT,  # URL of FECYT editor
    }
