# -*- encoding: utf-8 -*-

# Clase para importar documentos
from cvn.utilsCVN import *

# Modelos
from cvn.models import *

# Formularios
from cvn.forms import *

# Funciones de ayudas
from cvn.helpers import handle_old_cvn, getUserViinV, addUserViinV, getDataCVN

# Redireccion hacia otras paginas
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

#from django.exceptions import MultiKeyValueError

# Almacenar los ficheros subidos a la aplicación en el disco.
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Decorador
from django.contrib.auth.decorators import login_required

# Constantes para la importación de CVN
import cvn.settings as cvn_setts

# Fecha de subida del nuevo CVN
import datetime


# -- Vistas Aplicación CVN --
def index(request):
	""" Vista que ve el usuario cuando accede a la aplicación """
	print "INDEX"
	context = {}
	try:
		context['message'] = request.session['message']
		del request.session['message']
	except: # Puede que no exista el mensaje en la sesión
		pass 
	# Usuario CAS print context['user']['ou']	
	investCVN = None
	if not request.user.is_anonymous() and not request.user.is_staff:
		context['user'] = request.session['attributes'] 		
		invest, investCVN, investCVNname  = getUserViinV(context['user']['NumDocumento'])
		if not invest:
			# Se añade el usuario a la aplicación de ViinV
			invest = addUserViinV(context['user'])
		if investCVN:
			# Datos del CVN para mostrar e las tablas			
			context.update(getDataCVN(invest.nif))
			context['fecha_cvn'] = investCVN.fecha_cvn
			# Comprobar si el CVN no se ha actualizado en 6 meses
			context['file_cvn'] = investCVN.cvnfile	
			if (investCVN.fecha_cvn + datetime.timedelta(days = cvn_setts.CVN_CADUCIDAD)) < datetime.date.today():
				context['updateCVN'] = True
			else:				
				context['fecha_valido'] = investCVN.fecha_cvn + datetime.timedelta(weeks = 24)		
			
	# Envío del nuevo CVN
	if request.method == 'POST':		
		print "INDEX POST"
		context['form'] = UploadCvnForm(request.POST, request.FILES, instance = investCVN)				
		try:			
			if context['form'].is_valid() and (request.FILES['cvnfile'].content_type == cvn_setts.PDF):
				filePDF = request.FILES['cvnfile']			
				filePDF.name = setCVNFileName(invest)			
				# Se llama al webservice del Fecyt para corroborar que se trata de un CVN con el formato válido
				cvn = UtilidadesCVNtoXML(filePDF = filePDF)
				xmlFecyt = cvn.getXML(filePDF)
				userCVN  = cvn.checkCVNOwner(invest)
				if xmlFecyt and userCVN:
					handle_old_cvn(investCVNname, investCVN)				
					investCVN = context['form'].save(commit = False)
					investCVN.fecha_up = datetime.date.today()				
					investCVN.cvnfile.name = filePDF.name				
					investCVN.investigador = invest								
					xmlCVN = UtilidadesXMLtoBBDD(fileXML = filePDF.name.replace('pdf','xml'))
					investCVN.fecha_cvn = xmlCVN.insertarXML(invest) 				
					investCVN.save()										
					request.session['message'] = u'Se ha actualizado su CVN con éxito.'
					return HttpResponseRedirect(reverse("cvn.views.index"))					
				else:
					if not xmlFecyt:
						context['errors'] = u'El CVN no tiene formato FECYT'								
					elif not userCVN: 
						context['errors'] = u'El NIF/NIE del CVN no coincide con el del usuario de la sesión'
			else:		
				context['errors'] = u'El CVN tiene que ser un PDF.'		
		except KeyError:			
			context['errors'] = u'Seleccione un archivo'
	else:
		context['form'] = UploadCvnForm(instance = investCVN)		
	return render_to_response("index.html", context, RequestContext(request))

