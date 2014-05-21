# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.utils import scientific_production_to_context, cvn_to_context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
import logging

logger = logging.getLogger(__name__)


@login_required
def index(request):
    context = {}
    if 'attributes' in request.session:
        context['user'] = request.session['attributes']
    user = request.user
    form = UploadCVNForm()
    if request.method == 'POST':
        form = UploadCVNForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            form.save()
            context['message'] = _(u'CVN actualizado con éxito.')
    context['form'] = form
    cvn_to_context(user.profile, context)
    context['user'] = user
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
