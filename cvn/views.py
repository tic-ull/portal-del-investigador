# -*- encoding: UTF-8 -*-

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _
from forms import UploadCVNForm
from models import CVN
from statistics import settings as stSt
from utils import scientific_production_to_context, cvn_to_context
import logging
import settings as stCVN

logger = logging.getLogger(__name__)


@login_required
def index(request):
    context = {}
    user = request.user

    dept, dept_json = None, None
    if 'dept' and 'dept_json' in request.session:
        for obj in serializers.deserialize(
                "json", request.session['dept'], ignorenonexistent=True):
            dept = obj.object
        dept_json = request.session['dept_json']
        context['department'] = dept
        context['validPercentCVN'] = stSt.PERCENT_VALID_DEPT_CVN

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
            if dept is not None and old_cvn_status != cvn.status:
                dept.update(dept_json['departamento']['nombre'],
                            dept_json['miembros'], commit=True)

    context['form'] = form
    cvn_to_context(user.profile, context)
    context['CVN'] = scientific_production_to_context(user.profile, context)
    context['TIME_WAITING'] = stCVN.TIME_WAITING
    context['MESSAGES_WAITING'] = stCVN.MESSAGES_WAITING
    return render(request, 'cvn/index.html', context)


@login_required
def download_cvn(request):
    cvn = request.user.profile.cvn
    pdf = open(cvn.cvn_file.path)
    response = HttpResponse(pdf, mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s' % (
        cvn.cvn_file.name.split('/')[-1])
    return response


@login_required
@staff_member_required
def ull_report(request):
    context = {}
    user = User.objects.get(username='GesInv-ULL')
    scientific_production_to_context(user.profile, context)
    return render(request, 'cvn/ull_report.html', context)
