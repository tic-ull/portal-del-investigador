# -*- encoding: utf-8 -*-

# TODO Crear métodos para aquellos nodos como Telephone o Fax se repiten en todas las tablas y tiene un subárbol.

# Modelos BBDD
from cvn.models import *
# Conexión con la BBDD 'portalinvestigador'
from viinvDB.models import GrupoinvestInvestigador, GrupoinvestInvestcvn
# Parsear XML
from lxml import etree
# Excepción para la búsqueda de objetos en la BBDD
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned 
# Funciones de apoyo
from cvn.helpers import formatDocumentIdent, searchDataUser

import codecs # Para la codicación en utf-8
import suds # Web Service
import time # Para los sleep
import os
import errno
import binascii
import base64


class importCVN:
	"""
	Realiza la importación de los CVN creados con el editor del FECYT.
	- Obtiene la estructura XML de los PDFs.
	- Recorre el árbol XML y va introduciendo los datos en la BBDD.
	"""
	# Constantes con el usuario y pass para acceder al Web Service 
	# TODO Poner en el fichero "settings.py"
	USER_WS = "cvnPdfULL01"
	PASSWD_WS = "MXz8T9Py7Xhr"
	URL_BASE = "/../static/files/"
	URL_PDF = os.getcwd() + URL_BASE + "pdf/"
	URL_XML = os.getcwd() + URL_BASE + "xml/"
	URL_WS = "https://www.cvnet.es/cvn2RootBean_v1_3/services/Cvn2RootBean?wsdl"
	# Almacena las equivalencias entre los tags de los nodos XML y los campos de la BBDD
	DIC_TRANSLATE_XML = {
		u'GivenName': u'nombre',
		u'FirstFamilyName': u'primer_apellido',
		u'SecondFamilyName': u'segundo_apellido',
		u'Nacionality': u'nacionalidad',
		u'BirthDate': u'fecha_nacimiento',
		u'BirthCountry': u'pais_de_nacimiento',
		u'BirthRegion': u'comunidad_nacimiento',
		u'BirthCity': u'ciudad_de_nacimiento',
		u'Gender': u'sexo',
		u'City': u'ciudad_de_contacto',
		u'Streets': u'direccion',
		u'OtherInformation': u'resto_direccion',
		u'PostalCode': u'codigo_postal',
		u'Region':  u'comunidad',
		u'CountryCode': u'pais_de_contacto',
		u'Province': u'provincia',
		u'Telephone': u'telefono_',
		u'Fax': u'telefono_fax_',
		u'PersonalWeb': u'pagina_web_personal',
		u'InternetEmailAddress': u'correo_electronico',
		u'Photo': u'imagen',
	}
	
	# TODO Las variables por defecto se ob
	def __init__(self, urlPDF = URL_PDF, urlXML = URL_XML, urlWS = URL_WS):
		""" Constructor """		
		self.urlWS = urlWS
		self.clientWS = suds.client.Client(self.urlWS)
		
		self.urlPDF = urlPDF
		self.urlXML = urlXML
		
		# Se supone que existe el directorio donde se encuentran los PDFs
		self.__create_directory_XML__(self.urlXML)
		
			
	def __create_directory_XML__(self, path):
		"""
			Método privado que se encarga de crear el directorio donde se van a alojar
			los ficheros XMLs. En caso de que existan no crea dichos directorios.
			
			Parámetro:
			- path: Ruta donde se va a almacencar los ficheros 
		"""
		try:
			os.makedirs(path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise		
		
			
	def getXML(self, filePDF = "", urlXML = URL_XML):
		"""
			Método que a partir de un CVN en PDF obtiene su representación en XML,
			la cual almacena en el directorio especificado.
			
			Parámetros:
			- filePDF: Ruta y fichero PDF creado con el editor del FECYT.
			- urlXML: Ruta alternativa donde se almacena dicho XML. 
		"""			
		oldPdf = ""
		urlFile = self.urlPDF + filePDF
		#print urlFile
		# Se especifica la ruta hacia el fichero
		if len(filePDF.split('/')) > 1: 
			urlFile = filePDF
				
		# Se almacena el PDF en un array binario codificado en base 64
		try:
			dataPDF = binascii.b2a_base64(open(urlFile).read())
		except IOError:
			print u"No such file or directory:'" + urlFile + "'"
			return oldPdf

		# Se obtiene y almacena el fichero XML resultante
		fileXML = filePDF.replace("pdf", "xml")
		urlFile = self.urlXML + fileXML
		
		self.__create_directory_XML__(urlXML)
		urlFile = urlXML + "/" + fileXML
		
		# Llamada al Web Service para obtener la transformación a XML y la escribe a un fichero
		webServiceResponse = False
		while not webServiceResponse:
			try:
				resultXML = self.clientWS.service.cvnPdf2Xml(self.USER_WS, self.PASSWD_WS, dataPDF)
				webServiceResponse = True				
			except:
				print "No hay Respuesta para el fichero: "  + fileXML + ". Espera de 5 segundos para reintentar."
				time.sleep(5) 		
		
		if resultXML.errorCode == 0: # Formato CVN-XML del Fecyt
			dataXML = base64.b64decode(resultXML.cvnXml)
			fileXML = open(urlFile, "w").write(dataXML)
		else:
			print "File: '" + filePDF + "' no tiene el formato CVN-XML del Fecyt."
			oldPdf = filePDF # Retorna el fichero PDF con formato antiguo

		return oldPdf
			
			
	def getAllXML(self, urlPDF = URL_PDF, urlXML = URL_XML):
		"""
			Método que obtiene la estructura XML de todos los ficheros PDFs creados
			mediante el editor del Fecyt. Utiliza el método 'getXML' para obtener
			la representación XML de cada fichero.
			
			Parámetros:
			- urlPDF: Ruta hacia donde se encuentra los CVNs en formato PDF.
			- urlXML: Ruta alternativa donde se van a almacenar los XML resultantes.
		"""
		# Comprueba si se ha cambiado la ruta donde están los CVN en PDF		
		try:
			lista_cvn = os.listdir(urlPDF)
		except OSError:
			lista_cvn = []
			print u"No such file or directory:'" + urlPDF + "'"
		
		self.__create_directory_XML__(urlXML)
		cvnFile = codecs.open("../static/files/import/errorCVN.log", "w", "utf-8")
		if len(lista_cvn) > 0:
			# Recorre la lista que contiene los CVN en PDF y obtiene su representación en XML
			for cvn in lista_cvn:
				print cvn
				pdf = self.getXML(cvn, urlXML = urlXML)
				if pdf:
					cvnFile.write(pdf + '\n')
		cvnFile.close()
		
	
	def parseXML(self, fileXML = "", urlXML = URL_XML):
		"""
			Método que recorre el fichero XML y va extrayendo los datos del mismo.
			Dichos datos se almacenarán en la BBDD en las tablas correspondientes.
		"""
		#print urlXML + fileXML
		dic = {}
		try:
			tree = etree.parse(urlXML + fileXML)
			# Datos del Investigador
			dataInvest = tree.find('Agent')#/Identification/PersonalIdentification')			
			dic = self.__dataIdentificationXML__(dataInvest.getchildren())			
		except IOError:
			if fileXML:
				print u"Fichero " + fileXML + u" no encontrado."
			else:
				print u"Se necesita un fichero para ejecutar este método."		
		return dic
		

	def __dataIdentificationXML__(self, tree = None):
		"""
			Método privado para obtener los datos de identificación del usuario. 
			Incluye datos:
				- Personales
				- Dirección
				- Contacto
			Variable:
			- tree: Subárbol cuyo nodo cabecera es "Agent" del cual cuelgan todos los datos personales
		"""
		dic = {}
		for element in tree:
			if element.tag == u'Identification':				
				dic.update(self.__dataPersonalIdent__(element.getchildren()[0].getchildren()))
			if element.tag == u'Address':
				dic.update(self.__dataAddress__(element.getchildren()))				
			if element.tag == u'Contact':				
				dic.update(self.__dataContact__(element.getchildren()))
		return dic
		
		
	def __dataPersonalIdent__(self, tree = []):
		"""
			Método privado para introducir en un diccionario los datos personales del usuario.
			Variables:
			- tree: Lista de los nodos con la información personal del usuario.
		"""
		dic = {}
		for element in tree:
			if element.tag == u'OfficialId':
				dic['tipo_documento'] = element.getchildren()[0].tag
				dic['documento']      = u'' + element.getchildren()[0].getchildren()[0].text
			elif element.tag == u'BirthRegion':
				dic[self.DIC_TRANSLATE_XML[element.tag]] = u'' + element.getchildren()[1].getchildren()[0].text
			else:				
				# En caso de que sea un investigador extranjero no tiene segundo apellido
				try:
					dic[self.DIC_TRANSLATE_XML[element.tag]] = u'' + element.getchildren()[0].text
				except TypeError:
					pass
		return dic


	def __dataAddress__(self, tree = []):
		"""
			Método privado para introducir en un diccionario los datos de la dirección del usuario.
			Variables:
			- tree: Lista de los nodos con la información de la dirección del usuario.
		"""
		dic = {}
		for element in tree:
			if element.tag == u'Province' or element.tag == 'Region':				
				dic[self.DIC_TRANSLATE_XML[element.tag]] = u'' + element.getchildren()[1].getchildren()[0].text
			else:
				dic[self.DIC_TRANSLATE_XML[element.tag]] = u'' + element.getchildren()[0].text
		return dic
		

	def __dataContact__(self, tree = []):
		"""
			Método privado para introducir en un diccionario los datos de contacto del usuario.
			Variables:
			- tree: Lista de los nodos con la información de la contact del usuario.
		"""
		dic = {}		
		for element in tree:			
			key = self.DIC_TRANSLATE_XML[element.tag]
			if element.tag == u'Telephone' or element.tag == u'Fax':				
				if element.tag == u'Telephone':					
					if element.get('Type') == u'000':					
						key += 'fijo_'
					else:
						key += 'movil_'					
				for children in element.getchildren():
					if children.tag == u'InternationalCode':
						telephone_key = key + "cod"						
					if children.tag == u'Number':
						telephone_key = key + "num"						
					if children.tag == u'Extension':
						telephone_key = key + "ext"					
					dic[telephone_key] = children.getchildren()[0].text							
			else:
				dic[key] = u'' + element.getchildren()[0].text		
		return dic
	
			
	def updateInvestCVN(self, xmlFile = "", urlXML = URL_XML, user = None, fileError = None, fileCVN = None):
		"""
			Actualiza el campo 'xmlfile' de la tabla 'GrupoinvestInvestcvn' de la BBDD 'portalinvestigador'.
			Variables:
			- xmlFile: Fichero XML el cual se añade en la tabla.
			- urlXML: Ruta hacia donde están almacenados los ficheros XML.
			- user: Usuario CVN investigador a actualizar en la BBDD 'portalinvestigador'.
			- fileError: Fichero donde se almacenan los usuarios erróneos al actualizar.
			- fileCVN: Fichero donde se almacenarán aquellos CVN duplicados.
		"""		
		# Comprueba si ha cambiado la ruta
		data = urlXML + xmlFile
		if urlXML == self.URL_XML:			
			data = u"files/xml/" + xmlFile	
		nif_nie = formatDocumentIdent(user.documento)		
		try:			
			invest = GrupoinvestInvestigador.objects.get(nif__icontains = nif_nie)
			investcvn = GrupoinvestInvestcvn.objects.get(investigador = invest)
			# Comprueba que no ha sido actualizado
			if investcvn.xmlfile and investcvn.xmlfile != data:	
				fileCVN.write(u"Investigador con CVN duplicado: " + invest.nombre + " " + invest.apellido1 + "\n")
				fileCVN.write(u"Registro en la BBDD: " + investcvn.xmlfile + "\n")
				fileCVN.write(u"Registro duplicado: " + data + "\n")				
				fileCVN.write(u"---------------------------\n")
			else:				
				investcvn.xmlfile = data			
				investcvn.save()				
		except ValueError:			
			fileError.write(u"El investigador '" + user.nombre + " " + user.primer_apellido 
							+ u"' no ha introducido el DNI en el CVN.\n")
		except GrupoinvestInvestigador.DoesNotExist:			
			fileError.write(u"No existe el investigador con NIF/NIE: '"+ user.documento + "' (" + user.nombre + " " 
							+ user.primer_apellido + u") en la BBDD del Portal.\n")
		except GrupoinvestInvestcvn.DoesNotExist:
			fileError.write(u"No existe CVN para el investigador con NIF/NIE: '"+ user.documento + "' (" + user.nombre + " " 
							+ user.primer_apellido + u") en la BBDD del Portal.\n")		
		except MultipleObjectsReturned:	# Investigador duplicado
			fileError.write(u"El investigador '" + user.nombre + " " + user.primer_apellido + "' (NIF/NIE):" + user.documento
							+ u" está duplicado en la BBDD del portal\n")
	
	
	def parseAllXML(self, urlXML = URL_XML):
		"""
			Método que analiza todos los ficheros XML que se encuentran bajo la ruta
			especificada e introduce los datos en la BBDD.
			Variables:			
			- urlXML: Ruta donde están almacenados los ficheros XML.
		"""					
		data = {}
		# Comprueba si se ha cambiado la ruta donde están los CVN en PDF		
		try:
			lista_xml = os.listdir(urlXML)
		except OSError:
			lista_xml = []
			print u"No such file or directory:'" + urlXML + "'"
		
		fileError = codecs.open("../static/files/import/errorImport.log", "w", "utf-8")
		fileCVN   = codecs.open("../static/files/import/cvnDuplicados.log", "w", "utf-8")
		if len(lista_xml) > 0:
			# Recorre la lista que contiene los CVN en XML
			for xml in lista_xml:
				#print xml
				data = self.parseXML(xml, urlXML)				
				try:				
					# Comprueba si existe el usuario en la BBDD 
					# Nota: Se busca por los datos personales, pues algunos usuario carecen de NIF
					search = searchDataUser(data)					
					user = Usuario.objects.get(**search)																					
				except ObjectDoesNotExist:		
					# Usuario nuevo					
					user = Usuario.objects.create(**data)					
				self.updateInvestCVN(xml, urlXML, user, fileError, fileCVN)		
		fileError.close()
		fileCVN.close()
	
	
