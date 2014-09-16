# -*- encoding: UTF-8 -*-

from core.ws_utils import CachedWS as ws
from django.conf import settings as st
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django_tables2 import RequestConfig
from sigidi import SigidiConnection
from tables import (SummaryYearTable, SummaryConceptTable, BreakdownYearTable,
                    DetailTable, TotalConceptAndBreakdownTable,
                    TotalSummaryYearTable, AccountingTable)
from utils import total_table



@login_required
def index(request):
    context = dict()
    projects = []
    for project in SigidiConnection(request.user).get_projects():
        if 'CONT_KEY' in project and project['CONT_KEY'] is not None:
            projects.append(project)
    if projects is not None and len(projects):
        projects = AccountingTable(projects)
        RequestConfig(request, paginate=False).configure(projects)
        if not request.user.is_staff:
            projects.columns[2].column.visible = False
        context['projects'] = projects
    return render(request, 'accounting/index.html', context)


@login_required
def accounting_detail(request, code):
    context = dict()
    context['code'] = code
    project = SigidiConnection(user=request.user).get_project(code)

    if not project:
        raise Http404

    if 'CONT_KEY' in project and project['CONT_KEY'] is not None:
        accounting_code = project['CONT_KEY']

        if 'NAME' in project and project['NAME'] is not None:
            context['name'] = project['NAME']

        if ('ALLOW_CONTAB_RES' in project and
                project['ALLOW_CONTAB_RES'] is not None):

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
                RequestConfig(request, paginate=False).configure(breakdown_year)
                context['breakdown_year'] = breakdown_year
                context['total_breakdown_year'] = total_breakdown_year

        if ('ALLOW_CONTAB_LIST' in project and
                project['ALLOW_CONTAB_LIST'] is not None):

            detail = ws.get(st.WS_DETALLES % accounting_code)
            if detail is not None and len(detail):
                detail = DetailTable(detail)
                RequestConfig(request, paginate=False).configure(detail)
                context['detail'] = detail

    return render(request, 'accounting/accounting_detail.html', context)