# -*- encoding: utf-8 -*-

from cvn import settings as stCVN
from cvn.forms import UploadCvnForm
from cvn.helpers import (handleOldCVN, getUserViinV, addUserViinV,
                         getDataCVN, setCVNFileName)
from cvn.utilsCVN import (UtilidadesCVNtoXML, UtilidadesXMLtoBBDD)
from django.conf import settings as st
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import datetime
import logging

logger = logging.getLogger(__name__)


# -- Vistas Aplicación CVN --
def main(request):
    return HttpResponseRedirect(reverse('index'))


@login_required
def index(request):
    """ Vista que ve el usuario cuando accede a la aplicación """
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

    invest, investCVN = getUserViinV(context['user']['NumDocumento'])
    if not invest:
        # Se añade el usuario a la aplicación de ViinV
        invest = addUserViinV(context['user'])
    '''if investCVN:
        insert_pdf_to_bbdd_if_not_exists(
            context['user']['NumDocumento'], investCVN)
        # Datos del CVN para mostrar e las tablas
        context.update(getDataCVN(invest.nif))
        context.update(dataCVNSession(investCVN))'''
    logger.info("Acceso del investigador: " + invest.nombre + ' '
                + invest.apellido1 + ' ' + invest.apellido2 + ' ' + invest.nif)
    # Envío del nuevo CVN
    if request.method == 'POST':
        context['form'] = UploadCvnForm(request.POST,
                                        request.FILES,
                                        instance=investCVN)
        try:
            if context['form'].is_valid() and \
               (request.FILES['cvnfile'].content_type == stCVN.PDF):
                filePDF = request.FILES['cvnfile']
                filePDF.name = setCVNFileName(invest)
                # Se llama al webservice del FECYT para corroborar que
                # el CVN tiene formato válido
                cvn = UtilidadesCVNtoXML(filePDF=filePDF)
                xmlFecyt = cvn.getXML()
                # Si el CVN tiene formato FECYT y el usuario es el
                # propietario se actualiza
                if xmlFecyt and cvn.checkCVNOwner(invest, xmlFecyt, user):
                    if investCVN:
                        handleOldCVN(filePDF, investCVN.fecha_up)
                    investCVN = context['form'].save(commit=False)
                    investCVN.fecha_up = datetime.date.today()
                    investCVN.cvnfile = filePDF
                    investCVN.investigador = invest
                    # Borramos el viejo para que no se reenumere
                    if investCVN.xmlfile:
                        investCVN.xmlfile.delete()
                    investCVN.xmlfile.save(filePDF.name.replace('pdf', 'xml'),
                                           ContentFile(xmlFecyt), save=False)
                    #investCVN.fecha_cvn = UtilidadesXMLtoBBDD(
                    #    fileXML=investCVN.xmlfile
                    #).insertarXML(investCVN.investigador)
                    utils = UtilidadesXMLtoBBDD(fileXML=investCVN.xmlfile)
                    utils.insertarXML(investCVN.investigador, user)
                    investCVN.fecha_cvn = utils.getXMLDate()
                    investCVN.save()
                    request.session['message'] = u'Se ha actualizado su CVN \
                     con éxito.'
                    return HttpResponseRedirect(reverse("cvn.views.index"))
                else:
                    # Error PDF introducido no tiene el formato de la FECYT
                    if not xmlFecyt:
                        context['errors'] = u'El CVN no tiene formato FECYT'
                    # Error CVN no pertenece al usuario de la sesión
                    else:
                        context['errors'] = u'El NIF/NIE del CVN no coincide\
                                              con el del usuario.'
            else:        # Error cuando se envía un fichero que no es un PDF
                context['errors'] = u'El CVN tiene que ser un PDF.'
        # Error cuando se actualiza sin seleccionar un archivo
        except KeyError:
            context['errors'] = u'Seleccione un archivo'
    else:
        context['form'] = UploadCvnForm(instance=investCVN)
    return render_to_response("index.html", context, RequestContext(request))


@login_required
def downloadCVN(request):
    """ Descarga el CVN correspondiente al usuario logeado en la sesión """
    context = {}
    context['user'] = request.session['attributes']     # Usuario CAS
    invest, investCVN = getUserViinV(context['user']['NumDocumento'])
    if invest:  # El usuario para los test no se crea en la BBDD
        logger.info("Descarga CVN investigador: " + invest.nombre + ' '
                    + invest.apellido1 + ' ' + invest.apellido2 + ' '
                    + invest.nif)
    try:
        with open(st.MEDIA_ROOT + '/' + investCVN.cvnfile.name, 'r') as pdf:
            response = HttpResponse(pdf.read(), mimetype='application/pdf')
            response['Content-Disposition'] = 'inline;filename=%s' \
                % (investCVN.cvnfile.name.split('/')[-1])
        pdf.closed
    except (TypeError, IOError):
        raise Http404
    return response


@login_required
def ull_report(request):
    """ Informe completo de la actividad de la ULL,
        extraida del usuario especial ULL """
    context = {}
    context.update(getDataCVN('00000000A'))
    return render_to_response("ull_report.html", context,
                              RequestContext(request))
