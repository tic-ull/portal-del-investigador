# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.helpers import (handleOldCVN, setCVNFileName,
                         saveProductionToContext, dataCVNSession)
from cvn.models import FECYT, CVN
from django.conf import settings as st
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.template import RequestContext
import datetime
import logging

logger = logging.getLogger(__name__)


@login_required
def index(request):
    context = {}
    user = request.user
    #  Mensajes con información para el usuario
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
        context.update(dataCVNSession(cvn))
        saveProductionToContext(user.usuario, context)

    context['form'] = UploadCVNForm()
    if request.method == 'POST':
        form = UploadCVNForm(request.POST, request.FILES)
        if form.is_valid():
            filePDF = request.FILES['cvn_file']
            xmlFECYT = FECYT().getXML(filePDF)
            if xmlFECYT and CVN().checkCVNOwner(user, xmlFECYT):
                if cvn:
                    handleOldCVN(filePDF, cvn)
                    cvn.delete()
                if cvn and cvn.xml_file:
                    cvn.xml_file.delete()

                cvn = form.save(commit=False)
                cvn.fecha_up = datetime.date.today()
                filePDF.name = setCVNFileName(user)
                cvn.cvnfile = filePDF
                cvn.xml_file.save(filePDF.name.replace('pdf', 'xml'),
                                  ContentFile(xmlFECYT), save=False)
                cvn.fecha_cvn = CVN().getXMLDate(xmlFECYT)
                cvn.save()

                user.usuario.cvn = cvn
                user.usuario.save()
                cvn.insertXML(user)
                request.session['message'] = u'Se ha actualizado su CVN \
                 con éxito.'
                return HttpResponseRedirect(reverse("cvn.views.index"))
            else:
                if not xmlFECYT:
                    form.errors['cvn_file'] = ErrorList(
                        [u'El CVN no es válido para la FECYT.'])
                else:
                    form.errors['cvn_file'] = ErrorList(
                        [u'El NIF/NIE del CVN no coincide'
                         ' con el de su usuario.'])
        context['form'] = form

    return render(request, "index.html", context)


@login_required
def downloadCVN(request):
    """ Descarga el CVN correspondiente al usuario logeado en la sesión """
    user = request.user
    cvn = user.usuario.cvn
    if cvn:  # El usuario para los test no se crea en la BBDD
        logger.info("Descarga CVN investigador: " + user.username + ' '
                    + user.usuario.documento)
    try:
        with open(st.MEDIA_ROOT + '/' + cvn.cvn_file.name, 'r') as pdf:
            response = HttpResponse(pdf.read(), mimetype='application/pdf')
            response['Content-Disposition'] = 'inline;filename=%s' \
                % (cvn.cvn_file.name.split('/')[-1])
        pdf.closed
    except (TypeError, IOError):
        raise Http404
    return response


@login_required
def ull_report(request):
    """ Informe completo de la actividad de la ULL,
        extraida del usuario especial ULL """
    context = {}
    saveProductionToContext(request.user.usuario, context)
    return render(request, "ull_report.html", context)
