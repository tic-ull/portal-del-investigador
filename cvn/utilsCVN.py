# -*- encoding: utf-8 -*-

# TODO Crear métodos para aquellos nodos como Telephone o Fax se repiten en todas las tablas y tiene un subárbol.

# Importaciones auxiliares
import codecs # Para la codicación en utf-8
import suds   # Web Service
import time   # Sleep en caso de que haya un error de conexión
import os     
import errno
import binascii
import base64 # Codificación para el web service del Fecyt

# Modelo de la BBDD para la clase UtilidadesCVN
from cvn.models import *

# Conexión con la BBDD 'portalinvestigador'
from viinvDB.models import GrupoinvestInvestigador, GrupoinvestInvestcvn

# Parsear XML
from lxml import etree

# Excepción para la búsqueda de objetos en la BBDD
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned 

# Funciones de apoyo
from cvn.helpers import formatDocumentIdent, searchDataUser, formatCode, searchDataProduccionCientifica, formatDate, checkPage

# Constantes para la importación de CVN
import cvn.settings as cvn_setts




class UtilidadesCVN:
	"""
		Clase para el proceso en lotes de un directorio:
		 - Extracción de todos los CVN en formato PDF a XML.
		 - Inserción en la Base de Datos de los datos extraidos de los XML generados en el paso anterior.
	"""
	
	def __init__(self, urlPDF = cvn_setts.URL_PDF, urlXML = cvn_setts.URL_XML):
		""" Constructor """		
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
				
	
	
	def getAllXML(self):
		"""
			Método que obtiene la estructura XML de todos los ficheros PDFs creados
			mediante el editor del Fecyt. 
			Utiliza el método 'getXML' para obtener	la representación XML de cada fichero.			
		"""
		lista_cvn = os.listdir(self.urlPDF)
		cvnFile = codecs.open(cvn_setts.FILE_LOG_IMPORT, "w", "utf-8")
		# Recorre la lista que contiene los CVN en PDF y obtiene su representación en XML
		for cvn in lista_cvn:
			print cvn
			currentCVN = UtilidadesCVNtoXML(filePDF = cvn)
			result     = currentCVN.getXML()
			if not result: # En caso de que el CVN no tenga formato del Fecyt
				cvnFile.write(pdf + '\n')				
		cvnFile.close()

	def parseAllXML(self):
		"""
			Método que analiza todos los ficheros XML que se encuentran bajo la ruta
			especificada e introduce los datos en la BBDD.			
		"""					
		data = {}
		lista_xml = os.listdir(self.urlXML)		
		fileError = codecs.open(cvn_setts.FILE_LOG_ERROR, "w", "utf-8")
		fileCVN   = codecs.open(cvn_setts.FILE_LOG_DUPLICADOS, "w", "utf-8")
		# Recorre la lista que contiene los CVN en XML
		for xml in lista_xml:
			print "**************************************************************"
			print xml
			currentXML = UtilidadesXMLtoBBDD(fileXML = xml)
			# Retorna el usuario que se ha introducido en la BBDD
			user = currentXML.parseXML(fileError, fileCVN) 						
			print "**************************************************************"
		fileError.close()
		fileCVN.close()
		
	
# -----------------------		
class UtilidadesCVNtoXML:
	"""
		Clase que se encarga de acceder al Web Service de la Fecyt y obtener la respresentación en XML del CVN en PDF.	
		Parámetros:
		- url_ws: Dirección hacia el Web Service del Fecyt.
		- urlPDF: Ruta hacia donde están almacenados los PDF.
		- filePDF: Fichero PDF de donde va a extraer el XML.
	"""
	
	def __init__(self, 
				urlWS = cvn_setts.URL_WS, 
				urlPDF = cvn_setts.URL_PDF, 
				urlXML = cvn_setts.URL_XML,
				userWS = cvn_setts.USER_WS,
				passWS = cvn_setts.PASSWD_WS,
				filePDF = None):
		"""	Constructor """		
		self.urlWS   = urlWS		
		self.urlPDF  = urlPDF
		self.urlXML  = urlXML
		self.userWS  = userWS
		self.passWS  = passWS
		self.clientWS = suds.client.Client(self.urlWS)
		self.filePDF = filePDF
		

	def getXML(self):
		"""
			Método que a partir de un CVN en PDF obtiene su representación en XML.	
			
			Retorna el fichero si NO el PDF no tiene el formato del FECYT		
		"""				
		urlFile = self.urlPDF + self.filePDF								
		# Se almacena el PDF en un array binario codificado en base 64
		try:
			dataPDF = binascii.b2a_base64(open(urlFile).read())
		except IOError:
			print u"No such file or directory:'" + urlFile + "'"
			return False

		# Se obtiene y almacena el fichero XML resultante
		fileXML = self.filePDF.replace("pdf", "xml")
		urlFile = self.urlXML + fileXML
		
		# Llamada al Web Service para obtener la transformación a XML y la escribe a un fichero
		# Se añade la llamada en un bucle por si se corta la conexión con el servidor.
		webServiceResponse = False
		while not webServiceResponse:
			try:			
				resultXML = self.clientWS.service.cvnPdf2Xml(self.userWS, self.passWS, dataPDF)
				webServiceResponse = True				
			except:
				print "No hay Respuesta para el fichero: "  + self.filePDF + ". Espera de 5 segundos para reintentar."
				time.sleep(5) 		
		
		if resultXML.errorCode == 0: # Formato CVN-XML del Fecyt
			dataXML = base64.b64decode(resultXML.cvnXml)
			fileXML = open(urlFile, "w").write(dataXML)
		else:
			print "File: '" + filePDF + "' no tiene el formato CVN-XML del Fecyt."
			return False # Retorna el fichero PDF con formato antiguo
		
		return True


# -----------------------
class UtilidadesXMLtoBBDD:
	"""
		Esta clase provee los métodos necesarios para analizar los XML y almacenar los datos en la tablas de la BBDD.
	"""
	
	def __init__(self, 				
				urlXML  = cvn_setts.URL_XML,				
				fileXML = None):
		"""	Constructor """				
		self.urlXML  = urlXML		
		self.fileXML = fileXML
		
	
	def parseXML(self, fileError = "", fileCVN = ""):
		"""
			Método que recorre el fichero XML y va extrayendo los datos del mismo.
			Dichos datos se almacenarán en la BBDD en las tablas correspondientes.
			
			Variables:
			- fileError: Fichero donde se almacena los errores de importación
			- fileCVN: Fichero donde se almacenan aquellos cvn duplicados
		"""		
		user = None
		dataPersonal = {}
		try:
			tree = etree.parse(self.urlXML + self.fileXML)			
			# Datos del Investigador
			dataInvestigador = tree.find('Agent')  #/Identification/PersonalIdentification')			
			dataPersonal = self.__parseDataIdentificationXML__(dataInvestigador.getchildren())
			search = searchDataUser(dataPersonal)					
			user   = Usuario.objects.filter(**search)
			if not user:
				user = Usuario.objects.create(**dataPersonal)
			else:
				user = user[0] # Puede que encuentre varios usuarios debido a que algunos no introdujeron el NIF				
			#print user
			# Introduce los datos de la actividad científica
			self.__parseActividadCientifica__(user, tree.findall('CvnItem'))
			# Actualiza los datos en la BBDD del portal, tabla "GrupoinvestInvestCVN"
			self.updateInvestCVN(user, fileError, fileCVN)					
		except IOError:
			if self.fileXML:
				print u"Fichero " + self.fileXML + u" no encontrado."
			else:
				print u"Se necesita un fichero para ejecutar este método."		
		return user

	
	def __parseDataIdentificationXML__(self, tree = None):
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
			
			Variable:
			- tree: Lista de los nodos con la información personal del usuario.
		"""
		dic = {}
		for element in tree:
			if element.tag == u'OfficialId':
				dic['tipo_documento'] = element.getchildren()[0].tag
				dic['documento']      = u'' + formatDocumentIdent(element.getchildren()[0].getchildren()[0].text)
			elif element.tag == u'BirthRegion':
				dic[cvn_setts.DIC_PERSONAL_DATA_XML[element.tag]] = u'' + element.getchildren()[1].getchildren()[0].text
			else:				
				# En caso de que sea un investigador extranjero no tiene segundo apellido
				try:
					dic[cvn_setts.DIC_PERSONAL_DATA_XML[element.tag]] = u'' + element.getchildren()[0].text
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
				dic[cvn_setts.DIC_PERSONAL_DATA_XML[element.tag]] = u'' + element.getchildren()[1].getchildren()[0].text
			else:
				dic[cvn_setts.DIC_PERSONAL_DATA_XML[element.tag]] = u'' + element.getchildren()[0].text
		return dic
		

	def __dataContact__(self, tree = []):
		"""
			Método privado para introducir en un diccionario los datos de contacto del usuario.
			
			Variable:
			- tree: Lista de los nodos con la información de la contact del usuario.
		"""
		dic = {}		
		for element in tree:			
			key = cvn_setts.DIC_PERSONAL_DATA_XML[element.tag]
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


	def __getAutores__(self, tree = []):
		"""
			Método para obtener los datos de los autores participantes en Publicaciones, Artículos, ...
			
			Variable:
			- tree: Lista de los nodos con la información de los autores participantes.			
		"""
		lista_autores = ""
		for author in tree:
			if author.find("GivenName/Item") is not None and author.find("GivenName/Item").text is not None:
				lista_autores += u'' + author.find("GivenName/Item").text
			if author.find("FirstFamilyName/Item") is not None and author.find("FirstFamilyName/Item").text is not None:
				lista_autores += u' ' + author.find("FirstFamilyName/Item").text
			# Algunas veces el campo está creado pero sin ningún valor. El usuario introdujo un texto vacío.						
			if author.find("SecondFamilyName/Item") is not None and author.find("SecondFamilyName/Item").text is not None:
				lista_autores += u' ' + author.find("SecondFamilyName/Item").text
			# Este elemento se crea siempre al exportar el PDF al XML
			if author.find("Signature/Item").text is not None:
				lista_autores += u' (' + author.find("Signature/Item").text + '), '
			else:
				lista_autores += ', '
		return lista_autores[:-2]
	
	
	def __getAmbito__(self, tree = []):
		"""
			Método que extrae de la representación XML el ámbito de un Congreso, Proyecto o Convenio.
			
			Variable:
			- tree: Nodo que contiene los datos del ámbito.			
		"""
		data = {}
		if tree is not None:
			data['ambito'] = u'' + cvn_setts.SCOPE[tree.find('Type/Item').text]
			# Campo supuestamente obligatorio en el Editor de Fecyt, pero algunos PDFs no lo tienen.
			# Posiblemente es que se generaron con alguna versión anterior del editor.			
			if data['ambito'] == u"Otros" and (tree.find('Others/Item') is not None): 
				data['otro_ambito'] = u'' + tree.find('Others/Item').text 
		return data
		
		
	def __saveData__(self, user = None, data = {}, table = None):
		"""
			Método que se encarga de almacenar la actividad científica de un usuario en las tablas correspondientes.
			En caso de que exista ya dicho elemento almacenado en la tabla, simplemente se actualiza el campo usuario,
			añadiendo el nuevo usuario que se compartirá dicho mérito.
			
			Variables:
			- user: Usuario propietario de la actividad científica.
			- data: Datos a almacenar en la tabla correspondiente.			
			- table: Tabla donde se va a almacenar o actualizar los datos
		"""
		# Diccionario de búsqueda para comprobar si existe ya el dato en la tabla
		print data
		search_data = searchDataProduccionCientifica(data)			
		print search_data
		if not search_data: # Si devuelve un diccionario vacío, la búsqueda devuelve todos los registros de la tabla
			search_data = {'pk': cvn_setts.INVALID_SEARCH}
		try:				
			reg = table.objects.get(**search_data)
			print u"----------------------------------------------------> ENCONTRADO"
		except ObjectDoesNotExist: 
			# Se crea el nuevo registro en la tabla correspondiente
			#print data
			reg = table.objects.create(**data)
		# Añade el usuario a la tabla
		reg.usuario.add(user)
		
		#~ else:
			#~ #print "Tesis"
			#~ #print user
			#~ data.update({u'usuario': user})
			#~ #print data
			#~ table.objects.create(**data)
		

	def __getDataPublicacion__(sefl, tree = [], tipo = ""):
		"""
			Método que obtiene los siguientes datos de la publicacion:
			- Página inicial y final
			- Volumen y número
			Retorna un diccionario con dichos valores.
			
			Variable:
			- tree: Lista de los nodos con la información de los autores participantes.
			- tipo: Indica el tipo de producción, en caso de que se trate de un Artículo, 
			       se almacena los datos del Volumen y el Número.
		"""		
		data = {}		
		if tree is not None:
			if tree.find("Volume/Item") is not None:
				data['volumen'] = tree.find("Volume/Item").text
			if tree.find("Number/Item") is not None and tree.find("Number/Item").text is not None:
				data['numero']  = tree.find("Number/Item").text		
			#if tipo == u'Artículo':				
			if tree.find("InitialPage/Item") is not None and tree.find("InitialPage/Item").text is not None:					
				data['pagina_inicial'] = tree.find("InitialPage/Item").text #checkPage(tree.find("InitialPage/Item").text)
			if tree.find("FinalPage/Item") is not None and tree.find("FinalPage/Item").text is not None:
				data['pagina_final'] = tree.find("FinalPage/Item").text
		return data
			
			
	def __dataActividadCientificaPublicacion__(self, tree = []):
		"""
			Método que obtiene los datos de las publicaciones del usuario.
			Variable:
			- cvnpk: Identificador de la tabla de la Actividad Científica.
			- tree:  Elemento que contiene los datos necesarios de la publicación
			
			Return: Diccionario con los datos para introducir en la tabla "Publicación"
		"""
		#print "\n--- Publicaciones, documentos científicos y técnicos ---\n"		
		# Códigos de los atributos: Artículos (35), Capítulos (148), Libros (112)
		data = {}
		try:
			tipo = cvn_setts.ACTIVIDAD_CIENTIFICA_TIPO_PUBLICACION[tree.find('Subtype/SubType1/Item').text]						
			data[u'tipo_de_produccion'] = u'' + tipo
			if tree.find('Title/Name') is not None: # Hay CVN que no tienen puesta el título
				data[u'titulo'] = u'' + tree.find('Title/Name/Item').text		
			if tree.find('Link/Title/Name') is not None and tree.find('Link/Title/Name/Item').text is not None:
				data[u'nombre_publicacion'] = u'' + tree.find('Link/Title/Name/Item').text
			data[u'autores'] = self.__getAutores__(tree.findall('Author'))
			data.update(self.__getDataPublicacion__(tree.find('Location'), tipo))
			if tree.find('Date/OnlyDate/DayMonthYear') is not None: # Fecha: Dia/Mes/Año
				data[u'fecha'] = u'' + tree.find('Date/OnlyDate/DayMonthYear/Item').text
			elif tree.find('Date/OnlyDate/Year') is not None:       # Fecha: Año
				data[u'fecha'] = u'' + formatDate(tree.find('Date/OnlyDate/Year/Item').text)
			if tipo != u'Libro' and tree.find('ExternalPK') is not None:
				data[u'issn']  = u'' + tree.find('ExternalPK/Code/Item').text		
		except KeyError:       # El nodo no contiene ni artículos, ni capítulos ni libros.			
			pass
		except AttributeError: # El nodo no tiene especificado el tipo de Item.
			pass
		return data		


	def __dataActividadCientificaCongreso__(self, tree = []):
		"""
			Método que obtiene los datos de los congresos del usuario.
			Variable:
			- Tree: Lista de nodos con la información sobre las "Trabajos presentados en congresos nacionales o internacionales."
			
			Return: Diccionario con los datos para introducir en la tabla "Congreso"
		"""
		print "\n--- Trabajos presentados en congresos nacionales o internacionales ---\n"
		data = {}
		if tree.find('Title/Name') is not None: # Algonos trabajos no tienen puesto el nombre
			data[u'titulo'] = u'' + tree.find('Title/Name/Item').text		 
		for element in tree.findall('Link'):
			if element.find('CvnItemID/CodeCVNItem/Item').text == cvn_setts.DATA_CONGRESO:
				if element.find('Title/Name') is not None and element.find('Title/Name/Item').text is not None:
					data[u'nombre_del_congreso'] = u'' + element.find('Title/Name/Item').text
				# Fecha de realización
				if element.find('Date/OnlyDate/DayMonthYear') is not None: # Fecha: Dia/Mes/Año
					data[u'fecha_realizacion'] = u'' + element.find('Date/OnlyDate/DayMonthYear/Item').text
				elif element.find('Date/OnlyDate/Year') is not None:       # Fecha: Año
					data[u'fecha_realizacion'] = u'' + formatDate(element.find('Date/OnlyDate/Year/Item').text)
				# Fecha de finalización
				if element.find('Date/EndDate/DayMonthYear') is not None: # Fecha: Dia/Mes/Año
					data[u'fecha_finalizacion'] = u'' + element.find('Date/EndDate/DayMonthYear/Item').text
				elif element.find('Date/EndDate/Year') is not None:       # Fecha: Año
					data[u'fecha_finalizacion'] = u'' + formatDate(element.find('Date/EndDate/Year/Item').text)
				if element.find('Place/City') is not None:
					data[u'ciudad_de_realizacion'] = u'' + element.find('Place/City/Item').text
				# Ámbito
				data.update(self.__getAmbito__(element.find('Scope')))
				
		data[u'autores'] = self.__getAutores__(tree.findall('Author'))						
		return data
				
	
	def __dataExperienciaCientifica__(self, tree = [], tipo = ""):
		"""
			Método que obtiene los datos de tanto de la "participación en contratos, convenios 
			o proyectos	de I+D+i no competitivos con Administraciones o entidades públicas o privadas"
			como de "participación en proyectos de I+D+i financiados en convocatorias competitivas de
			Administraciones o entidades públicas y privadas".	
 .
			Variable:
			- tree: Lista de nodos con la información sobre los convenios.
			- tipo: Indica si se trata de un Convenio o un Proyecto
			
			Return: Diccionario con los datos para introducir en la tabla "Publicación"		
		"""
		print "\n --- Convenios y Proyectos de I+D+i ---\n"
		data = {}
		if tree.find('Title/Name') is not None: # Hay CVN que no tienen puesta la denominación del proyecto
			data[u'denominacion_del_proyecto'] = u'' + tree.find('Title/Name/Item').text
		
		# Según se trate de un convenio o proyecto la fecha inicial cuelga de un nodo diferente
		nodo = "StartDate"
		if cvn_setts.MODEL_TABLE[tipo] == Convenio:
			nodo = "OnlyDate"
		
		# Fecha de inicio Convenios y Proyectos
		if tree.find('Date/' + nodo + '/DayMonthYear') is not None: # Fecha: Dia/Mes/Año
			data[u'fecha_de_inicio'] = u'' + tree.find('Date/' + nodo + '/DayMonthYear/Item').text
		elif tree.find('Date/' + nodo + '/Year') is not None:       # Fecha: Año
			data[u'fecha_de_inicio'] = u'' + formatDate(tree.find('Date/' + nodo + '/Year/Item').text)
		
		# Fecha final Proyectos
		if cvn_setts.MODEL_TABLE[tipo] == Proyecto: 				
			if tree.find('Date/EndDate/DayMonthYear') is not None and tree.find('Date/EndDate/DayMonthYear/Item').text is not None: 
				data[u'fecha_de_fin'] = u'' + tree.find('Date/EndDate/DayMonthYear/Item').text			
			elif tree.find('Date/EndDate/Year') is not None and tree.find('Date/EndDate/Year/Item').text is not None: 
				data[u'fecha_de_fin'] = u'' + formatDate(tree.find('Date/EndDate/Year/Item').text)
				
		# La duración del proyecto viene codificada en el siguiente formato:P <num_years> Y <num_months> M <num_days> D
		# TODO Decodificar el codigo de duración 
		if tree.find('Date/Duration') is not None:
			duration_code = u'' + tree.find('Date/Duration/Item').text 		
			# TODO Calcular fecha final a partir de la duración si se trata de un Convenio
			
		data[u'autores'] = self.__getAutores__(tree.findall('Author'))
		
		# Dimensión Económica
		for element in tree.findall('EconomicDimension'):
			economic_code = element.find('Value').attrib['code']
			data[cvn_setts.ECONOMIC_DIMENSION[economic_code]] =  u'' + element.find('Value/Item').text
		if tree.find('ExternalPK/Code') is not None:
			data[u'cod_segun_financiadora'] = u'' + tree.find('ExternalPK/Code/Item').text
		
		# Ámbito 
		data.update(self.__getAmbito__(tree.find('Scope')))
		return data
		

	def __dataActividadDocente__(self, tree = []):
		"""
			Método para obtener los datos de la Actividad docente de un usuario.
			Sección del Editor "Dirección de tesis doctorales y/o proyectos fin de carrera".
			
			Variable:
			- tree: Lista de nodos con la información necesaria para obtener los datos de la tesis
		
			Return: Diccionario con los datos a insertar en la tabla correspondiente
		"""
		data = {}		
		# Comprueba si la actividad docente se trata de una tesis
		try:
			if tree.find('Subtype/SubType1/Item').text == cvn_setts.DATA_TESIS:
				#print "\n--- Dirección de tesis doctorales y/o proyectos fin de carrera ---\n"
				data[u'titulo'] = u'' + tree.find('Title/Name/Item').text
				data[u'universidad_que_titula'] = u'' + tree.find('Entity/EntityName/Item').text			
				data[u'autor'] = self.__getAutores__(tree.findall('Author'))
				data[u'codirector'] = self.__getAutores__(tree.findall('Link/Author'))	
				data[u'fecha_de_lectura'] = u'' + tree.find('Date/OnlyDate/DayMonthYear/Item').text
		except AttributeError: # No tiene elemento tipo: 'Subtype/SubType1/Item'
			pass
		return data		
		
	
			
	def __parseActividadCientifica__(self, user = None, cvnItems = []):
		"""
			Método para obtener los datos de la Actividad científica de un usuario.
			Recorre el XML buscando aquellos nodos 'CVNItem' cuyo 'CvnItemID/CVNPK' se engloban dentro de '060.XXX.XXX.XXX'.			
			Variable:
			- user: Usuario del CVN
			- cvnItems: Lista de los nodos con la información de los méritos almacenada en el CVN.
		"""		
		# Recorre los méritos introducidos en el CVN por el investigador 
		for element in cvnItems:
			data = {}
			cvn_key = element.find('CvnItemID/CVNPK/Item').text			
			#print "---------------- " + str(cvn_key) + " ----------------"				
			# Actividad docente (Paso 4 Editor Fecyt)
			if cvn_key == u"030.040.000.000":				
				data = self.__dataActividadDocente__(element)
			# Experiencia científica y tecnológica (Paso 5 Editor Fecyt)
			if cvn_key == u"050.020.020.000" or cvn_key == u"050.020.010.000":
				data = self.__dataExperienciaCientifica__(element, cvn_key)
			# Actividad científica y tecnológica (Paso 6 Editor Fecyt)			
			if cvn_key == u"060.010.010.000": # Publicación, documentos científicos y técnicos				
				data = self.__dataActividadCientificaPublicacion__(element)					
			if cvn_key == u"060.010.020.000": # Trabajos presentados en congresos nacionales o internacionales.				
				data = self.__dataActividadCientificaCongreso__(element)			
			# Almacena los datos
			if data:
				#print data
				self.__saveData__(user, data, cvn_setts.MODEL_TABLE[cvn_key])						
		


	def updateInvestCVN(self, user = None, fileError = None, fileCVN = None):
		"""
			Actualiza el campo 'xmlfile' de la tabla 'GrupoinvestInvestcvn' de la BBDD 'portalinvestigador'.
			Variables:			
			- user: Usuario CVN investigador a actualizar en la BBDD 'portalinvestigador'.
			- fileError: Fichero donde se almacenan los usuarios erróneos al actualizar.
			- fileCVN: Fichero donde se almacenarán aquellos CVN duplicados.
		"""		
		
		#data = self.urlXML + self.fileXML		
		data = u"files/xml/" + self.fileXML		
		nif_nie = formatDocumentIdent(user.documento)		
		try:			
			invest    = GrupoinvestInvestigador.objects.get(nif__icontains = nif_nie)
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
		except ValueError:			                    # Usuario sin DNI en el CVN introducido en el Fecyt
			fileError.write(u"El investigador '" + user.nombre + " " + user.primer_apellido 
							+ u"' no ha introducido el DNI en el CVN.\n")
		except GrupoinvestInvestigador.DoesNotExist:	# Investigador no existe en la BBDD del Portal Viinv.		
			fileError.write(u"No existe el investigador con NIF/NIE: '"+ user.documento + "' (" + user.nombre + " " 
							+ user.primer_apellido + u") en la BBDD del Portal.\n")
		except GrupoinvestInvestcvn.DoesNotExist:       # Investigador sin registro de CVN en la BBDD del Portal Viinv
			fileError.write(u"No existe CVN para el investigador con NIF/NIE: '"+ user.documento + "' (" + user.nombre + " " 
							+ user.primer_apellido + u") en la BBDD del Portal.\n")		
		except MultipleObjectsReturned:	                # Investigador duplicado
			fileError.write(u"El investigador '" + user.nombre + " " + user.primer_apellido + "' (NIF/NIE):" + user.documento
							+ u" está duplicado en la BBDD del portal\n")
