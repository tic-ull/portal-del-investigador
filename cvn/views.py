# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.utils import scientific_production_to_context, date_cvn_to_context
from django.conf import settings as st
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
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
    user = request.user
    cvn = user.profile.cvn
    if cvn:
        logger.info("Download CVN: " + user.username + ' - '
                    + user.profile.documento)
    try:
        filename = st.MEDIA_ROOT + '/' + cvn.cvn_file.name
        download_name = cvn.cvn_file.name.split('/')[-1]
        with open(filename, 'r') as pdf:
            response = HttpResponse(pdf.read(), mimetype='application/pdf')
            response['Content-Disposition'] = 'inline; filename=%s' % (
                download_name)
        pdf.closed
    except (TypeError, IOError):
        raise Http404
    return response


@login_required
def ull_report(request):
    context = {}
    scientific_production_to_context(request.user.profile, context)
    return render(request, 'ull_report.html', context)
