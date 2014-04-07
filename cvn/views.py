# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.models import FECYT, CVN
from cvn.utils import saveScientificProductionToContext, getDataCVN, movOldCVN
from django.conf import settings as st
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
import logging

logger = logging.getLogger(__name__)


@login_required
def index(request):
    context = {}
    user = request.user
    if 'message' in request.session:
        context['message'] = request.session['message']
        del request.session['message']

    if 'attributes' in request.session:
        context['user'] = request.session['attributes']
    else:
        return HttpResponseRedirect(reverse('logout'))
    cvn = user.usuario.cvn
    if cvn:
        context['CVN'] = True
        context.update(getDataCVN(cvn))
        saveScientificProductionToContext(user.usuario, context)

    context['form'] = UploadCVNForm()
    if request.method == 'POST':
        formCVN = UploadCVNForm(request.POST, request.FILES)
        if formCVN.is_valid():
            filePDF = request.FILES['cvn_file']
            (xmlFECYT, errorCode) = FECYT().getXML(filePDF)
            if xmlFECYT and CVN().checkCVNOwner(user, xmlFECYT):
                if cvn:
                    movOldCVN(cvn)
                    cvn.delete()
                if cvn and cvn.xml_file:
                    cvn.xml_file.delete()
                cvn = formCVN.save(user=user, fileXML=xmlFECYT, commit=False)
                cvn.save()
                user.usuario.cvn = cvn
                user.usuario.save()
                cvn.insertXML(user)
                context['message'] = _(u'CVN actualizado con éxito.')
            else:
                if not xmlFECYT:
                    formCVN.errors['cvn_file'] = ErrorList(
                        [_(u'El CVN no es válido para la FECYT.')])
                else:
                    formCVN.errors['cvn_file'] = ErrorList(
                        [_(u'El NIF/NIE del CVN no coincide'
                           ' con el de su usuario.')])
        context['form'] = formCVN
    return render(request, "index.html", context)


@login_required
def download_cvn(request):
    user = request.user
    cvn = user.usuario.cvn
    if cvn:
        logger.info("Download CVN: " + user.username + ' - '
                    + user.usuario.documento)
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
    """ Informe completo de la actividad de la ULL,
    extraida del usuario especial ULL """
    context = {}
    saveScientificProductionToContext(request.user.usuario, context)
    return render(request, "ull_report.html", context)
