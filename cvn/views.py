# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.utils import scientific_production_to_context, cvn_to_context
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#
from django.conf import settings as st
from statistics.settings import PERCENT_VALID_DEPT_CVN
from statistics.utils import calc_stats_department
#
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _
import json
import logging
import urllib

logger = logging.getLogger(__name__)


@login_required
def index(request):
    context = {}
    user = request.user
    form = UploadCVNForm()
    if request.method == 'POST':
        form = UploadCVNForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            form.save()
            context['message'] = _(u'CVN actualizado con éxito.')
    context['form'] = form
    cvn_to_context(user.profile, context)
    context['CVN'] = scientific_production_to_context(user.profile, context)
    # STATS
    WS = '%sget_departamento_y_miembros?cod_persona=%s'\
         % (st.WS_SERVER_URL, user.profile.rrhh_code)
    try:
        department = json.loads(urllib.urlopen(WS).read())
        context['stats'] = {'department': department['departamento']['nombre']}
        context['stats'].update(calc_stats_department(department['miembros']))
        context['validPercentCVN'] = PERCENT_VALID_DEPT_CVN
    except IOError:  # WS down
        pass
    except KeyError:  # Test users
        pass
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
