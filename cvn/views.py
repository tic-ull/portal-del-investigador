# -*- encoding: utf-8 -*-

from cvn import settings as stCVN
from cvn.forms import UploadCvnForm
from cvn.helpers import (handleOldCVN, getDataCVN,
                         setCVNFileName, dataCVNSession)
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
    #  TODO: Obtener cvn de usuario con bbdd actual
    cvn = user.usuario.cvn
    if cvn:
        context.update(getDataCVN(user.usuario))
        context.update(dataCVNSession(cvn))

    # Envío del nuevo CVN
    if request.method == 'POST':
        context['form'] = UploadCvnForm(request.POST,
                                        request.FILES)
        try:
            if context['form'].is_valid() and \
               (request.FILES['cvn_file'].content_type == stCVN.PDF):
                filePDF = request.FILES['cvn_file']
                filePDF.name = setCVNFileName(user)
                # Se llama al webservice del FECYT para corroborar que
                # el CVN tiene formato válido
                util = UtilidadesCVNtoXML(filePDF=filePDF)
                xmlFecyt = util.getXML()
                # Si el CVN tiene formato FECYT y el usuario es el
                # propietario se actualiza
                if xmlFecyt and util.checkCVNOwner(user, xmlFecyt):
                    if cvn:
                        handleOldCVN(filePDF, cvn)
                        # se elimina el registro con el CVN antiguo
                        cvn.delete()
                    cvn = context['form'].save(commit=False)
                    cvn.fecha_up = datetime.date.today()
                    cvn.cvn_file = filePDF
                    #cvn.investigador = invest
                    #cvn.owner = user
                    # Borramos el viejo para que no se reenumere
                    if cvn.xml_file:
                        cvn.xml_file.delete()
                    cvn.xml_file.save(filePDF.name.replace('pdf', 'xml'),
                                      ContentFile(xmlFecyt), save=False)
                    utils = UtilidadesXMLtoBBDD(fileXML=cvn.xml_file)
                    utils.insertarXML(user)
                    cvn.fecha_cvn = utils.getXMLDate()
                    cvn.save()
                    user.usuario.cvn = cvn
                    user.usuario.save()
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
        context['form'] = UploadCvnForm()
    return render_to_response("index.html", context, RequestContext(request))


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
    context.update(getDataCVN('00000000A'))
    return render_to_response("ull_report.html", context,
                              RequestContext(request))
