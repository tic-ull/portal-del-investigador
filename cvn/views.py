# -*- encoding: UTF-8 -*-

from django.conf import settings as st
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils.translation import ugettext as _
from forms import UploadCVNForm, GetDataCVNULL
from models import CVN
from utils import (scientific_production_to_context, cvn_to_context,
                   stats_to_context)
from cvn import settings as st_cvn
import datetime


@login_required
def index(request):
    context = {}
    user = request.user
    dept, dept_json, area, area_json = stats_to_context(request, context)
    try:
        cvn = CVN.objects.get(user_profile__user=user)
        old_cvn_status = cvn.status
    except ObjectDoesNotExist:
        cvn = None
        old_cvn_status = None

    form = UploadCVNForm()
    if request.method == 'POST':
        form = UploadCVNForm(request.POST, request.FILES,
                             user=user, instance=cvn)
        if form.is_valid():
            cvn = form.save()
            context['message'] = _(u'CVN actualizado con éxito.')
            if old_cvn_status != cvn.status:
                if dept is not None:
                    dept.update(dept_json['unidad']['nombre'],
                                dept_json['miembros'], commit=True)
                if area is not None:
                    area.update(area_json['unidad']['nombre'],
                                area_json['miembros'], commit=True)

    context['form'] = form
    cvn_to_context(user.profile, context)
    context['CVN'] = scientific_production_to_context(user.profile, context)
    context['TIME_WAITING'] = st_cvn.TIME_WAITING
    context['MESSAGES_WAITING'] = st_cvn.MESSAGES_WAITING
    return render(request, 'cvn/index.html', context)


@login_required
def download_cvn(request):
    cvn = request.user.profile.cvn
    pdf = open(cvn.cvn_file.path)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s' % (
        cvn.cvn_file.name.split('/')[-1])
    return response


@login_required
@staff_member_required
def ull_report(request, year):
    if year is None or year not in st.HISTORICAL:
        raise Http404
    context = {}
    user = User.objects.using(st.HISTORICAL[year]).get(username='GesInv-ULL')
    scientific_production_to_context(user.profile, context)
    try:
        context['report_date'] = unicode(year)
    except ObjectDoesNotExist:
        context['report_date'] = _('No disponible')
    return render(request, 'cvn/ull_report.html', context)


@login_required
def export_data_ull(request):
    if not request.user.profile.rrhh_code:
        raise Http404

    context = dict()
    context['form'] = GetDataCVNULL()

    if request.method == 'POST':
        form = GetDataCVNULL(request.POST)
        if form.is_valid():
            start_year = None
            end_year = None

            if 'select_year' in form.data:
                form_year = int(form.data['year'])
                start_year = datetime.date(form_year, 01, 01)
                end_year = datetime.date(form_year, 12, 31)
            if 'range_years' in form.data:
                form_start_year = int(form.data['start_year'])
                start_year = datetime.date(form_start_year, 01, 01)
                end_year = datetime.date(int(form.data['end_year']), 12, 31)

            pdf = CVN.get_user_pdf_ull(request.user, start_year, end_year)

            if not pdf:
                form._errors['__all__'] = _(
                    u'No dispone de información en el periodo seleccionado')
                context['form'] = form
                return render(request, 'cvn/export_data_ull.html', context)

            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = (
                'attachment;' 'filename="CVN-EXPORT-%s.pdf"' % (
                    request.user.profile.documento))
            return response

        context['form'] = form
    return render(request, 'cvn/export_data_ull.html', context)
