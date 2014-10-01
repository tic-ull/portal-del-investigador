# -*- encoding: UTF-8 -*-

from core.ws_utils import CachedWS as ws
from django.conf import settings as st
from django.contrib.auth.decorators import login_required
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import render
from django_tables2 import RequestConfig
from sigidi import SigidiConnection
from tables import (SummaryYearTable, SummaryConceptTable, BreakdownYearTable,
                    DetailTable, TotalConceptAndBreakdownTable,
                    TotalSummaryYearTable, AccountingTableProjects,
                    AccountingTableAgreements)
from utils import total_table, clean_accounting_table


@login_required
def index(request):
    context = dict()
    try:
        sigidi = SigidiConnection(request.user)
    except OperationalError:
        return render(request, 'core/503.html', context)

    manager_projects = sigidi.can_view_all_projects()
    if manager_projects:
        list_projects = sigidi.get_all_projects()
    else:
        list_projects = sigidi.get_user_projects()

    context['projects'] = clean_accounting_table(
        request=request, data=list_projects,
        table_class=AccountingTableProjects, role=manager_projects)

    manager_agreements = sigidi.can_view_all_convenios()
    if manager_agreements:
        list_agreements = sigidi.get_all_convenios()
    else:
        list_agreements = sigidi.get_user_convenios()

    context['agreements'] = clean_accounting_table(
        request=request, data=list_agreements,
        table_class=AccountingTableAgreements, role=manager_agreements)

    context['active_projects'] = "active"
    if "sort" in request.GET and "convenio" in request.GET['sort']:
        context['active_agreements'] = "active"
        context['active_projects'] = ""
    return render(request, 'accounting/index.html', context)


@login_required
def accounting_detail(request, code):
    context = dict()
    context['code'] = code
    try:
        if code.startswith('PR'):
            entity = SigidiConnection(user=request.user).get_project(code)
        else:
            entity = SigidiConnection(user=request.user).get_convenio(code)
    except OperationalError:
        return render(request, 'core/503.html', context)

    if not entity:
        raise Http404

    if 'NAME' in entity and entity['NAME'] is not None:
        context['name'] = entity['NAME']

    if 'CONT_KEY' in entity and entity['CONT_KEY'] is not None:
        accounting_code = entity['CONT_KEY']

        if ('ALLOW_CONTAB_RES' in entity and
                entity['ALLOW_CONTAB_RES'] is not None):

            summary_year = ws.get(st.WS_RESUMEN_YEAR % accounting_code)
            if summary_year is not None and len(summary_year):
                total_summary_year = total_table(
                    request=request, data=summary_year,
                    table_class=TotalSummaryYearTable)
                summary_year = SummaryYearTable(summary_year)
                RequestConfig(request, paginate=False).configure(summary_year)
                context['summary_year'] = summary_year
                context['total_summary_year'] = total_summary_year

            summary_concept = ws.get(st.WS_RESUMEN_CONCEPTO % accounting_code)
            if summary_concept is not None and len(summary_concept):
                total_summary_concept = total_table(
                    request=request, data=summary_concept,
                    table_class=TotalConceptAndBreakdownTable)
                summary_concept = SummaryConceptTable(summary_concept)
                RequestConfig(
                    request, paginate=False).configure(summary_concept)
                context['summary_concept'] = summary_concept
                context['total_summary_concept'] = total_summary_concept

            breakdown_year = ws.get(st.WS_DESGLOSE_YEAR % accounting_code)
            if breakdown_year is not None and len(breakdown_year):
                total_breakdown_year = total_table(
                    request=request, data=breakdown_year,
                    table_class=TotalConceptAndBreakdownTable)
                breakdown_year = BreakdownYearTable(breakdown_year)
                RequestConfig(
                    request, paginate=False).configure(breakdown_year)
                context['breakdown_year'] = breakdown_year
                context['total_breakdown_year'] = total_breakdown_year

        if ('ALLOW_CONTAB_LIST' in entity and
                entity['ALLOW_CONTAB_LIST'] is not None):

            detail = ws.get(st.WS_DETALLES % accounting_code)
            if detail is not None and len(detail):
                detail = DetailTable(detail)
                RequestConfig(request, paginate=False).configure(detail)
                context['detail'] = detail

    return render(request, 'accounting/accounting_detail.html', context)
