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
import datetime

# Modelo de la BBDD para la clase UtilidadesCVN
from cvn.models import *

# Conexión con la BBDD 'portalinvestigador'
from viinvDB.models import GrupoinvestInvestigador, GrupoinvestInvestcvn

# Parsear XML
from lxml import etree

# Excepción para la búsqueda de objetos en la BBDD
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned 

# Funciones de apoyo
from cvn.helpers import formatNIF, searchDataUser, formatCode, searchDataProduccionCientifica, formatDate, checkPage

# Constantes para la importación de CVN
import cvn.settings as cvn_setts

# Logs
import logging
logger = logging.getLogger(__name__)
from  django.db.models.loading import get_model

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
		

	def getXML(self, memoryCVNFile = None):
		"""
			Método que a partir de un CVN en PDF obtiene su representación en XML.	
			
			Retorna el fichero si NO el PDF no tiene el formato del FECYT		
		"""		
		if not memoryCVNFile:				
			urlFile = self.urlPDF + str(self.filePDF)			
			fileXML = self.filePDF.replace("pdf", "xml")			
			
		# Se almacena el PDF en un array binario codificado en base 64
		try:
			if not memoryCVNFile:				
				dataPDF = binascii.b2a_base64(open(urlFile).read())
			else:
				dataPDF = binascii.b2a_base64(memoryCVNFile.read())
				fileXML = memoryCVNFile.name
				fileXML = fileXML.replace('pdf','xml')
		except IOError:
			logger.error(u"No such file or directory:'" + urlFile + "'")			
			return False

		# Se almacena el fichero XML resultante		
		urlFile = self.urlXML + fileXML
		
		# Llamada al Web Service para obtener la transformación a XML y la escribe a un fichero
		# Se añade la llamada en un bucle por si se corta la conexión con el servidor.
		webServiceResponse = False
		while not webServiceResponse:
			try:			
				resultXML = self.clientWS.service.cvnPdf2Xml(self.userWS, self.passWS, dataPDF)
				webServiceResponse = True				
			except:
				logger.warning("No hay Respuesta para el fichero: "  + self.filePDF + ". Espera de 5 segundos para reintentar.")				
				time.sleep(5) 		
		
		if resultXML.errorCode == 0: # Formato CVN-XML del Fecyt
			dataXML = base64.b64decode(resultXML.cvnXml)
			fileXML = open(urlFile, "w").write(dataXML)
		else:						
			return False # Retorna el fichero PDF con formato antiguo		
		return True


	def checkCVNOwner(self, user = None):
		"""
			Este método se encarga de corroborar que el propietario del CVN es el mismo que está logeado en la sesión.
		"""		
		data = {}
		nif = ''
		fileXML = self.filePDF.name.replace("pdf", "xml")
		try:			
			tree = etree.parse(self.urlXML + fileXML)					
			nif = tree.find('Agent/Identification/PersonalIdentification/OfficialId/DNI/Item')
			if nif is not None  and nif.text is not None:
				nif = nif.text
			else:
				nif = tree.find('Agent/Identification/PersonalIdentification/OfficialId/NIE/Item')
				if nif is not None and nif.text is not None:
					nif = nif.text
			if nif and nif.upper() == user.nif.upper():
				return True
		except IOError:			
			if fileXML:				
				logger.error("Fichero " + fileXML + u" no encontrado.")				
			else:
				logger.warning(u"Se necesita un fichero para ejecutar este método.")				
		return False
		
		
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
		
	
	def parseXML(self):#, fileBBDD = "", fileCVN = ""):
		"""
			Método que recorre el fichero XML y va extrayendo los datos del mismo.
			Dichos datos se almacenarán en la BBDD en las tablas correspondientes.
			
			Variables:
			- fileBBDD: Fichero donde se almacena los CVN almacenados en la importación
			- fileCVN: Fichero donde se almacenan aquellos cvn duplicados
		"""			
		cvn = cvn_setts.RUTA_BBDD + self.fileXML.replace("xml", "pdf")		
		# Comprobar si existe ya el CVN en el portal del investigador.
		cvn_investigador = GrupoinvestInvestcvn.objects.filter(cvnfile__icontains = cvn.split('/')[-1])		
		if len(cvn_investigador) > 0:			
			# Se inserta los datos del usuario en la BBDD de la aplicación CVN y se actualiza la columna CVN			
			fecha_cvn = self.insertarXML(cvn_investigador[0].investigador)
			# Se actualiza la columna 'xmlfile'
			cvn_investigador[0].xmlfile = cvn_setts.RUTA_BBDD + self.fileXML
			cvn_investigador[0].fecha_cvn = fecha_cvn
			cvn_investigador[0].save()
			# Se actualiza el fichero con CVN insertados
			logger.info(u'' + cvn + ',' + cvn_investigador[0].investigador.nombre + ' ' +
						cvn_investigador[0].investigador.apellido1 + ' ' +
						cvn_investigador[0].investigador.apellido2 + ',' + 
						cvn_investigador[0].investigador.nif + '\n')
		else:
			# Se realiza una valoración del contenido del xml y se calcula la valoración	
			(lista, probabilidad) = self.valorarXML()
			if lista is not None and lista:			
				for usuario in lista:
					logger.warning(u'' + self.fileXML + ',' + 
								usuario.cod_persona + ',' + 
								usuario.nombre + ' ' + usuario.apellido1 + ' ' + usuario.apellido2 + ',' + 
								usuario.nif + ',')
					try: # Busca el CVN que tiene almacenado en Viinv del posible usuario candidato.
						invest = GrupoinvestInvestigador.objects.get(nif = usuario.nif)
						cvn_viinv = GrupoinvestInvestcvn.objects.get(investigador= invest)
						logger.warning(u'' + str(cvn_viinv.cvnfile) + ',')
						#~ fileCVN.write(u'' + str(cvn_viinv.cvnfile) + ',')
					except ObjectDoesNotExist:
						logger.warning(u'UNKNOWN, ')
						#~ fileCVN.write(u'UNKNOWN, ')

					logger.warning(u'' + str(probabilidad) + '\n')
			else: # No coincide el NIF con ningun investigador alojado en la BBDD.		
				logger.warning(u'' + self.fileXML + ', ' + 
							'UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN, ' + 
							str(probabilidad) + '\n')
			
				
	def get_key_data(self, filename):
		""" 
			return a tuple with key data extracted from a CVN XML:
			date_CVN, dni, nombre_completo, birth_date, email
		"""
		tree = etree.parse(filename)
		date_CVN = tree.find('Version/VersionID/Date/Item')
		if date_CVN is not None:
			date_CVN  = date_CVN.text
		nombre = u''
		nombre += tree.find('Agent/Identification/PersonalIdentification/GivenName/Item').text

		first_family_name = tree.find('Agent/Identification/PersonalIdentification/FirstFamilyName/Item')
		if first_family_name.text is not None:
			first_family_name = u'' + first_family_name.text
		
		segundo_apellido = None
		second_family_name = tree.find('Agent/Identification/PersonalIdentification/SecondFamilyName/Item')
		if second_family_name is not None:
			second_family_name = u'' + unicode(second_family_name.text)
		
		birth_date = tree.find('Agent/Identification/PersonalIdentification/BirthDate/Item')
		if birth_date is not None:
			birth_date = birth_date.text
		   
		nif = tree.find('Agent/Identification/PersonalIdentification/OfficialId/DNI/Item')
		if nif is not None:
			nif = nif.text
		else:
			nif = tree.find('Agent/Identification/PersonalIdentification/OfficialId/NIE/Item')
			if nif is not None:
				nif = nif.text
		
		email = tree.find('Agent/Contact/InternetEmailAddress/Item')
		if email is not None:
			email = email.text

		return (date_CVN, nif, nombre, first_family_name, second_family_name, birth_date, email)	
		
		
	def valorarXML(self):
		""" 
			Valora la probabilidad de que CVN pertenezca a un usuario registrado en el portal de ViinV 
			
			Return: 		
			- lista_usuario: Lista de usuarios posibles como propietarios del CVN analizado
			- probabilidad: Medida de 0 a 1.
		"""
		probabilidad = 0		
		(date_CVN, nif, nombre, primer_apellido, segundo_apellido, birth_date, email) = self.get_key_data(self.urlXML + self.fileXML)
		# Se eliminan los datos erróneos que pueda contener el dni (en caso de que lo tenga introducido)
		nif = formatNIF(nif)
		if nif is not None:
			usuario = GrupoinvestInvestigador.objects.filter(nif = nif)
			if usuario:
				probabilidad = 1
				return (usuario, probabilidad)
			else:
				return (None, 0)
		# No dispone de NIF se aplican otros baremos de matching		
		lista_usuarios = GrupoinvestInvestigador.objects.filter(apellido1__iexact = primer_apellido)
		if lista_usuarios is not None:
			probabilidad += 0.2
		# Se filtra la lista inicial por el segundo apellido
		if segundo_apellido is not None:
			lista_aux = lista_usuarios.filter(apellido2__iexact = segundo_apellido)
			if lista_aux:
				probabilidad += 0.3
				lista_usuarios = lista_aux
		else:
			probabilidad += 0.3
		# Se filtra la lista inicial por el nombre
		lista_aux = lista_usuarios.filter(nombre__icontains = nombre)
		if lista_aux is not None:
			probabilidad += 0.3
			lista_usuarios = lista_aux
		# Se filtra la lista por la fecha de nacimiento
		if birth_date is not None:
			birth_date = datetime.date(int(birth_date.split("-")[0]), 
										int(birth_date.split("-")[1]), 
										int(birth_date.split("-")[2]))
			lista_aux = lista_usuarios.filter(fecha_nacimiento = birth_date)
			if lista_aux is not None:
				probabilidad += 0.075
				lista_usuarios = lista_aux
		# Se filtra la lista por el correo electrónico
		lista_aux = lista_usuarios.filter(email = email)
		if lista_aux is not None:
			probabilidad += 0.075
			lista_usuarios = lista_aux
		# Se devuelve la lista de usuarios con la probabilidad de que sean propietarios del CVN analizado	
		return (lista_usuarios, probabilidad)
	
	
	def __deleteOldData__(self, data = [], user = None):
		"""
			Recorre la lista de datos donde el usuario tiene una referencia o es la única referencia hacia los mismos.
			Si es la única referencia se elimina los datos, sino sólo se elimina la referencia.
		"""
		for actividad in data:
			if actividad.usuario.count() > 1:
				actividad.usuario.remove(user)				
			else:
				actividad.delete()				
				
				
	def __cleanDataCVN__(self, user = None): 
		"""
			Elimina los datos introducidos previamente por el usuario. En caso que los datos pertenezcan a
			varios usuarios, se elimina sólo las referencias del usuario a los mismos.
			
			Variables:
			- user -> Usuario que está introduciendo un nuevo CVN.			
		"""
		# Actividad científica
		self.__deleteOldData__(Publicacion.objects.filter(usuario = user), user)		
		self.__deleteOldData__(Congreso.objects.filter(usuario = user), user)
		self.__deleteOldData__(Proyecto.objects.filter(usuario = user), user)
		self.__deleteOldData__(Convenio.objects.filter(usuario = user), user)
		self.__deleteOldData__(TesisDoctoral.objects.filter(usuario = user), user)
		
	
		
	def insertarXML(self, investigador = None):
		""" 
			Inserta los datos del CVN encontrados en el portal en la base de datos de la aplicación CVN 
			
			Variables:
			- investigador -> Usuario con el que se enlaza ambas BBDD.
		"""		
		dataPersonal = {}
		fecha_cvn = None		
		try:			
			tree = etree.parse(self.urlXML + self.fileXML)			
			fecha_cvn = tree.find('Version/VersionID/Date/Item').text			
			# Datos del Investigador
			dataInvestigador = tree.find('Agent')  #/Identification/PersonalIdentification')			
			dataPersonal = self.__parseDataIdentificationXML__(dataInvestigador.getchildren())
			search_data = searchDataUser(dataPersonal)			
			if search_data:				
				search_user = Usuario.objects.filter(**search_data)								
				if not search_user:					
					#dataPersonal.update({'investigador': investigador})
					user = Usuario.objects.create(**dataPersonal)
				else:
					user = search_user[0]
					# Si el usuario ha introducido datos son eliminados para introducir los nuevos
					# TODO ....
				# Introduce los datos de la actividad científica
				self.__parseActividadCientifica__(user, tree.findall('CvnItem'))
			else:
				logger.warning("CVN sin datos personales:  " + str(self.fileXML))				
		except IOError:
			if self.fileXML:
				logger.error("Fichero " + self.fileXML + u" no encontrado.")				
			else:
				logger.warning(u"Se necesita un fichero para ejecutar este método.")				
		return fecha_cvn

	
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
			if element.tag == u'Identification' and element.getchildren():
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
				dic['documento']      = u'' + formatNIF(element.getchildren()[0].getchildren()[0].text)
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
		lista_autores = ''		
		for author in tree:
			auxAuthor = ''
			if author.find("GivenName/Item") is not None and author.find("GivenName/Item").text is not None:
				auxAuthor = u'' + author.find("GivenName/Item").text				
			if author.find("FirstFamilyName/Item") is not None and author.find("FirstFamilyName/Item").text is not None:
				auxAuthor += u' ' + author.find("FirstFamilyName/Item").text				
			# Algunas veces el campo está creado pero sin ningún valor. El usuario introdujo un texto vacío.						
			if author.find("SecondFamilyName/Item") is not None and author.find("SecondFamilyName/Item").text is not None:
				auxAuthor += u' ' + author.find("SecondFamilyName/Item").text				
			# Este elemento se crea siempre al exportar el PDF al XML
			if author.find("Signature/Item").text is not None:
				if auxAuthor: # Si tiene datos, la firma va entre paréntesis
					lista_autores += auxAuthor + u' (' + author.find("Signature/Item").text + '); '
				else:         # El único dato de los autores es la firma
					lista_autores += u'' + author.find("Signature/Item").text + '; '
			else:
				lista_autores += auxAuthor + '; '
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
		
	
	def __getDuration__(self, code = ""):
		"""
			Método que devuelve la duración de un convenio. El código tiene el siguiente formato:
			  "P<años>Y<meses>M<dias>D"
			  
			Variable:
			- code: Cadena de texto con el código de duración del convenio
		"""
		digit = ""
		data = {}
		for c in code[1:]: # El primero carácter P se salta.
			if c.isdigit():
				digit += c
			else:								
				if c == 'Y':
					data['duracion_anyos'] = u'' + digit
				if c == 'M':
					data['duracion_meses'] = u'' + digit
				if c == 'D':
					data['duracion_dias']  = u'' + digit
				digit = ""				
		return data
		
		
	def __saveData__(self, user = None, data = {}, table_name = None):
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
		search_data = searchDataProduccionCientifica(data)					
		if not search_data: # Si devuelve un diccionario vacío, la búsqueda devuelve todos los registros de la tabla
			search_data = {'pk': cvn_setts.INVALID_SEARCH}
		table = get_model('cvn', table_name)
		try:				
			reg = table.objects.get(**search_data)
			# Actualiza el registro con los nuevos datos
			table.objects.filter(pk = reg.id).update(**data)				
		except ObjectDoesNotExist: 
			# Se crea el nuevo registro en la tabla correspondiente			
			reg = table.objects.create(**data)
		# Añade el usuario a la tabla
		reg.usuario.add(user)
			

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
			Publicaciones, documentos científicos y técnicos
		
			Método que obtiene los datos de las publicaciones del usuario.
			Variable:
			- cvnpk: Identificador de la tabla de la Actividad Científica.
			- tree:  Elemento que contiene los datos necesarios de la publicación
			
			Return: Diccionario con los datos para introducir en la tabla "Publicación"
		"""		
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
			Trabajos presentados en congresos nacionales o internacionales
			
			Método que obtiene los datos de los congresos del usuario.
			Variable:
			- Tree: Lista de nodos con la información sobre las "Trabajos presentados en congresos nacionales o internacionales."
			
			Return: Diccionario con los datos para introducir en la tabla "Congreso"
		"""		
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
			Convenios y Proyectos de I+D+i
		
			Método que obtiene los datos de tanto de la "participación en contratos, convenios 
			o proyectos	de I+D+i no competitivos con Administraciones o entidades públicas o privadas"
			como de "participación en proyectos de I+D+i financiados en convocatorias competitivas de
			Administraciones o entidades públicas y privadas".	
 
			Variable:
			- tree: Lista de nodos con la información sobre los convenios.
			- tipo: Indica si se trata de un Convenio o un Proyecto
			
			Return: Diccionario con los datos para introducir en la tabla "Publicación"		
		"""
		data = {}
		if tree.find('Title/Name') is not None: # Hay CVN que no tienen puesta la denominación del proyecto
			data[u'denominacion_del_proyecto'] = u'' + tree.find('Title/Name/Item').text
		
		# Posibles nodos donde se almacena la fecha
		if tree.find('Date/StartDate'):
			nodo = "StartDate"
		else:
			nodo = "OnlyDate"
		# Según se trate de un convenio o proyecto la fecha inicial cuelga de un nodo diferente
		#~ if cvn_setts.MODEL_TABLE[tipo] == Convenio:
			#~ nodo = "OnlyDate"
		
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
		if tree.find('Date/Duration') is not None and tree.find('Date/Duration/Item').text is not None:
			duration_code = u'' + tree.find('Date/Duration/Item').text 		
			data.update(self.__getDuration__(duration_code))
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
			Dirección de tesis doctorales y/o proyectos fin de carrera
		
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
				self.__saveData__(user, data, cvn_setts.MODEL_TABLE[cvn_key])								
	

# -----------------------	
def checkUserCVN(data = "", cvn = None):
	"""
		Comprueba si el usuario que accede a la aplicación tiene introducido los datos de su CVN.
		Si no es así, introduce los datos generando previamente el XML
		
		Variables:
		- data = NIF/NIE del usuario
		- cvn  = Registro de la tabla GrupoinvestInvestcvn de la aplicación ViinV
	"""		
	
	if not Usuario.objects.filter(documento__icontains = data):		
		handlerCVN = UtilidadesCVNtoXML(filePDF = cvn.cvnfile.name.split('/')[-1])
		xmlFecyt = handlerCVN.getXML() 				
		if xmlFecyt:
			cvn.xmlfile = cvn_setts.RUTA_BBDD + cvn.cvnfile.name.split('/')[-1].replace('pdf', 'xml')
		xmlCVN = UtilidadesXMLtoBBDD(fileXML = cvn.cvnfile.name.split('/')[-1].replace('pdf', 'xml'))
		xmlCVN.insertarXML(cvn.investigador)
		cvn.save()
	
