# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.utils import (scientific_production_to_context,
                       cvn_to_context,
                       calc_stats_department,)
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#
from django.conf import settings as st
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cvn.settings import PERCENT_VALID_DEPT_CVN
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
    WS = '%sget_departamento_y_miembros?cod_persona=%s'\
         % (st.WS_SERVER_URL, user.profile.rrhh_code)
    department = json.loads(urllib.urlopen(WS).read())
    context['stats'] = {'department': department['departamento']['nombre']}
    context['stats'].update(calc_stats_department(department['miembros']))
    context['validPercenCVN'] = PERCENT_VALID_DEPT_CVN
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


@ login_required
@staff_member_required
def stats_report(request):
    # Access to data in memory, cache...
    context = {}
    departmentStats = [{'numCVNupdate': 0,
                        'cvnPercentUpdated': 5,
                        'numMembers': 27,
                        'departamento': u'ANATOMIA, ANAT.\
                        PATOLÓGICA E HISTOLOGÍA'},
                       {'numCVNupdate': 0,
                        'cvnPercentUpdated': 80,
                        'numMembers': 20,
                        'departamento': 'ANÁLISIS ECONÓMICO'},
                       {'numCVNupdate': 15,
                        'cvnPercentUpdated': 71,
                        'numMembers': 20,
                        'departamento': 'BECARIOS'},
                       {'numCVNupdate': 15,
                        'cvnPercentUpdated': 71,
                        'numMembers': 20,
                        'departamento': 'DEPT1'},
                       {'numCVNupdate': 15,
                        'cvnPercentUpdated': 91,
                        'numMembers': 27,
                        'departamento': 'DEPT2'},
                       {'numCVNupdate': 35,
                        'cvnPercentUpdated': 75,
                        'numMembers': 89,
                        'departamento': 'DEPT3'},
                       {'numCVNupdate': 0,
                        'cvnPercentUpdated': 100,
                        'numMembers': 43,
                        'departamento': 'ANÁLISIS MATEMÁTICO'}]
    # Paginator- Show X department per page
    paginator = Paginator(departmentStats, 3)
    page = request.GET.get('page')
    try:
        department_list = paginator.page(page)
    except PageNotAnInteger:
        department_list = paginator.page(1)
    except EmptyPage:
        department_list = paginator.page(paginator.num_pages)
    context['departmentStats'] = department_list
    context['validPercenCVN'] = PERCENT_VALID_DEPT_CVN
    return render(request, 'cvn/stats_report.html', context)
