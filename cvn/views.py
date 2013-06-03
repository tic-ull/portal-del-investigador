# -*- encoding: utf-8 -*-

from django.http import HttpResponse
# Clase para importar documentos
from cvn.importCVN import *
# Modelos
from cvn.models import *

def index(request):
	""" Vista que importa los datos desde los PDFs """
	importToBBDD = importCVN()
	#~ importToBBDD.getAllXML()
		
	print "--------------> index()"
	#importToBBDD.parseAllXML()
	
	
	#~ data = importToBBDD.parseXML("CVN-jujepere-475f2c19.xml")
	#~ print data
	#~ user = Usuario.objects.create(**data)
	#~ importToBBDD.updateInvestCVN("CVN-jujepere-475f2c19.xml", importToBBDD.URL_XML, user)
	return HttpResponse("Importación de CVN en formato PDFs")
