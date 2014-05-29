# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.utils import scientific_production_to_context, cvn_to_context
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
import logging

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
    return render(request, 'cvn/index.html', context)


@login_required
def download_cvn(request):
    cvn = request.user.profile.cvn
    pdf = open(cvn.cvn_file.path, 'r')
    response = HttpResponse(pdf, mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s' % (
        cvn.cvn_file.name.split('/')[-1])
    return response


@login_required
@staff_member_required
def ull_report(request):
    context = {}
    userULL = User.objects.get(username='GesInv-ULL')
    scientific_production_to_context(userULL.profile, context)
    return render(request, 'cvn/ull_report.html', context)


@login_required
@staff_member_required
def stats_report(request):
    # Access to data in memory, cache...
    context = {}
#    context['departmentStats'] = [{'numCVNupdate': 0,
#                                   'cvnPercentUpdated': 35,
#                                   'numMembers': 27,
#                                   'departamento': u'ANATOMIA, ANAT.\
#                                   PATOLÓGICA E HISTOLOGÍA'},
#                                  {'numCVNupdate': 0,
#                                   'cvnPercentUpdated': 80,
#                                   'numMembers': 20,
#                                   'departamento': 'ANÁLISIS ECONÓMICO'},
#                                  {'numCVNupdate': 0,
#                                   'cvnPercentUpdated': 10,
#                                   'numMembers': 43,
#                                   'departamento': 'ANÁLISIS MATEMÁTICO'}]
    departmentStats = [{'numCVNupdate': 0,
                        'cvnPercentUpdated': 35,
                        'numMembers': 27,
                        'departamento': u'ANATOMIA, ANAT.\
                        PATOLÓGICA E HISTOLOGÍA'},
                       {'numCVNupdate': 0,
                        'cvnPercentUpdated': 80,
                        'numMembers': 20,
                        'departamento': 'ANÁLISIS ECONÓMICO'},
                       {'numCVNupdate': 0,
                        'cvnPercentUpdated': 10,
                        'numMembers': 43,
                        'departamento': 'ANÁLISIS MATEMÁTICO'}]
    # Paginator- Show 2 department per page
    paginator = Paginator(departmentStats, 2)
    page = request.GET.get('page')
    try:
        department_list = paginator.page(page)
    except PageNotAnInteger:
        department_list = paginator.page(1)
    except EmptyPage:
        department_list = paginator.page(paginator.num_pages)
    context['departmentStats'] = department_list
    return render(request, 'cvn/stats_report.html', context)
