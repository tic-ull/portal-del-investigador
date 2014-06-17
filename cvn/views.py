# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.utils import scientific_production_to_context, cvn_to_context
from cvn.models import CVN
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from statistics.models import Department
import statistics.settings as stSt
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
import json
import logging
import urllib

logger = logging.getLogger(__name__)


@login_required
def index(request):
    context = {}
    user = request.user
    form = UploadCVNForm()

    # Get department code of the user from webservice, and with it,
    # find the department statistics on database
    try:
        dept_json = json.loads(urllib.urlopen(stSt.WS_INFO_USER %
                                              user.profile.rrhh_code).read())
        dept = Department.objects.get(
            code=dept_json['departamento']['cod_departamento'])
    except (IOError, KeyError):  # WS down, user without dept
        dept = None

    if request.method == 'POST':
        form = UploadCVNForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            try:
                old_status = CVN.objects.get(user_profile__user=user).status
            except ObjectDoesNotExist:
                old_status = None
            new_status = form.save().status
            if old_status != new_status and dept is not None:
                dept.update(dept_json['departamento']['nombre'],
                            dept_json['miembros'], True)
            context['message'] = _(u'CVN actualizado con éxito.')
    context['form'] = form
    cvn_to_context(user.profile, context)
    context['CVN'] = scientific_production_to_context(user.profile, context)
    context['department'] = dept
    context['validPercentCVN'] = stSt.PERCENT_VALID_DEPT_CVN
    return render(request, 'cvn/index.html', context)


@login_required
def download_cvn(request):
    cvn = request.user.profile.cvn
    pdf = open(cvn.cvn_file.path, 'r')
    response = HttpResponse(pdf, mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s' % (
        cvn.cvn_file.name.split('/')[-1])
    return response


@ login_required
@staff_member_required
def ull_report(request):
    context = {}
    userULL = User.objects.get(username='GesInv-ULL')
    scientific_production_to_context(userULL.profile, context)
    return render(request, 'cvn/ull_report.html', context)
