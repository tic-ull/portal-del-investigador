# -*- encoding: UTF-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sigidi import SigidiConnection
from core.ws_utils import CachedWS as ws
from django.conf import settings as st


@login_required
def index(request):
    context = {}
    return render(request, 'accounting/base.html', context)


@login_required
def accounting_detail(request, code):
    context = {}
    context['code'] = code
    project = SigidiConnection(user=request.user).get_project(code)
    if 'CONT_KEY' in project and project['CONT_KEY'] is not None:
        if ('ALLOW_CONTAB_RES' in project and
                project['ALLOW_CONTAB_RES'] is not None):
            context['resumen_year'] = ws.get(st.WS_RESUMEN_YEAR % code)
            context['resumen_concepto'] = ws.get(st.WS_RESUMEN_CONCEPTO % code)
            context['desglose_year'] = ws.get(st.WS_DESGLOSE_YEAR % code)
        if ('ALLOW_CONTAB_LIST' in project and
                project['ALLOW_CONTAB_LIST'] is not None):
            context['detalles'] = ws.get(st.WS_DETALLES % code)
    return render(request, 'accounting/accounting_detail.html', context)
