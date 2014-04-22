# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.utils import scientific_production_to_context, date_cvn_to_context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
import logging

logger = logging.getLogger(__name__)


@login_required
def index(request):
    context = {}
    if 'message' in request.session:
        context['message'] = request.session['message']
        del request.session['message']
    if 'attributes' in request.session:
        context['user'] = request.session['attributes']
    user = request.user
    context['form'] = UploadCVNForm()
    if request.method == 'POST':
        form = UploadCVNForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            form.save()
            context['message'] = _(u'CVN actualizado con éxito.')
        context['form'] = form
    date_cvn_to_context(user.profile.cvn, context)
    context['CVN'] = scientific_production_to_context(user.profile, context)
    return render(request, 'index.html', context)


@login_required
def download_cvn(request):
    cvn = request.user.profile.cvn
    pdf = open(cvn.cvn_file.path, 'r')
    response = HttpResponse(pdf, mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s' % (
        cvn.cvn_file.name.split('/')[-1])
    return response


@login_required
def ull_report(request):
    context = {}
    scientific_production_to_context(request.user.profile, context)
    return render(request, 'ull_report.html', context)
