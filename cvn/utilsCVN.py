# -*- encoding: utf-8 -*-

# TODO Crear métodos para aquellos nodos como Telephone o Fax
# se repiten en todas las tablas y tiene un subárbol.
from django.db.models.loading import get_model
from django.core.files.base import ContentFile
from cvn.helpers import (formatNIF, searchDataUser,
                         searchDataProduccionCientifica, formatDate)
from cvn.models import (Usuario, Publicacion, Congreso,
                        Proyecto, Convenio, TesisDoctoral)
from django.core.exceptions import ObjectDoesNotExist
from lxml import etree
import base64  # Codificación para el web service del FECYT
import datetime
import cvn.settings as st
import logging
import suds   # Web Service
import time   # Sleep en caso de que haya un error de conexión

logger = logging.getLogger(__name__)


# -----------------------
class UtilidadesCVNtoXML:
    """
        Clase que se encarga de acceder al Web Service de la FECYT y
        obtener la representación en XML del CVN en PDF.
        Parámetros:
        - url_ws: Dirección hacia el Web Service del FECYT.
        - urlPDF: Ruta hacia donde están almacenados los PDF.
        - filePDF: Fichero PDF de donde va a extraer el XML.
    """

    def __init__(self,
                 urlWS=st.URL_WS,
                 urlPDF=st.URL_PDF,
                 urlXML=st.URL_XML,
                 userWS=st.USER_WS,
                 passWS=st.PASSWD_WS,
                 filePDF=None):
        """ Constructor """
        self.urlWS = urlWS
        self.urlPDF = urlPDF
        self.urlXML = urlXML
        self.userWS = userWS
        self.passWS = passWS
        self.clientWS = suds.client.Client(self.urlWS)
        self.filePDF = filePDF

    def getXML(self):
        """
            Método que a partir de un CVN en PDF obtiene su
            representación en XML.

            Retorna el XML o False si el PDF no tiene el formato del FECYT
        """
        # Se almacena el PDF en un array binario codificado en base 64
        try:
            dataPDF = base64.encodestring(self.filePDF.read())
        except IOError:
            logger.error(u"No such file or directory:'"
                         + self.filePDF.name + "'")
            return False

        # Llamada al Web Service para obtener la transformación a XML
        # y la escribe a un fichero. Se añade la llamada en un bucle por si
        # se corta la conexión con el servidor.
        webServiceResponse = False
        while not webServiceResponse:
            try:
                resultXML = self.clientWS.service.cvnPdf2Xml(self.userWS,
                                                             self.passWS,
                                                             dataPDF)
                webServiceResponse = True
            except:
                logger.warning("No hay Respuesta para el fichero: "
                               + self.filePDF
                               + ". Espera de 5 segundos para reintentar.")
                time.sleep(5)

        if resultXML.errorCode == 0:  # Formato CVN-XML del FECYT
            return base64.decodestring(resultXML.cvnXml)
        return False  # Retorna el fichero PDF con formato antiguo

    def checkCVNOwner(self, user=None, fileXML=None):
        """
            Este método se encarga de corroborar que el propietario del CVN
            es el mismo que está logeado en la sesión.
        """
        if not fileXML:
            logger.warning(u"Se necesita un fichero\
                            para ejecutar este método.")
            return False
        try:
            tree = etree.XML(fileXML)
        except IOError:
            logger.error("Fichero XML no encontrado.")
            return False

        nif = tree.find('Agent/Identification/'
                        'PersonalIdentification/OfficialId/DNI/Item')
        if nif is not None and nif.text is not None:
            nif = nif.text.strip()
        else:
            nif = tree.find('Agent/Identification/'
                            'PersonalIdentification/OfficialId/NIE/Item')
            if nif is not None and nif.text is not None:
                nif = nif.text.strip()
        if nif: # and nif.upper() == user.nif.upper():
            return True
        return False


class UtilidadesXMLtoBBDD:
    """
        Esta clase provee los métodos necesarios para analizar los XML y
        almacenar los datos en la tablas de la BBDD.
    """

    def __init__(self,
                 urlXML=st.URL_XML,
                 fileXML=None):
        """ Constructor """
        self.urlXML = urlXML
        self.fileXML = fileXML
        self.tree = etree.parse(self.fileXML)

    def get_key_data(self, filename):
        """
            return a tuple with key data extracted from a CVN XML:
            date_CVN, dni, nombre_completo, birth_date, email
        """
        tree = etree.parse(filename)
        date_CVN = tree.find('Version/VersionID/Date/Item')
        if date_CVN is not None:
            date_CVN = date_CVN.text.strip()
        nombre = u''
        nombre += tree.find('Agent/Identification/PersonalIdentification/'
                            'GivenName/Item').text.strip()

        first_family_name = tree.find(
            'Agent/Identification/PersonalIdentification/FirstFamilyName/Item'
        )
        if first_family_name.text is not None:
            first_family_name = u'' + first_family_name.text.strip()

        second_family_name = tree.find(
            'Agent/Identification/PersonalIdentification/SecondFamilyName/Item'
        )
        if second_family_name is not None:
            second_family_name = u'' + unicode(second_family_name.text.strip())

        birth_date = tree.find('Agent/Identification/PersonalIdentification/'
                               'BirthDate/Item')
        if birth_date is not None:
            birth_date = birth_date.text.strip()

        nif = tree.find('Agent/Identification/PersonalIdentification/'
                        'OfficialId/DNI/Item')
        if nif is not None:
            nif = nif.text.strip()
        else:
            nif = tree.find('Agent/Identification/PersonalIdentification/'
                            'OfficialId/NIE/Item')
            if nif is not None:
                nif = nif.text.strip()

        email = tree.find('Agent/Contact/InternetEmailAddress/Item')
        if email is not None:
            email = email.text.strip()

        return (date_CVN, nif, nombre, first_family_name,
                second_family_name, birth_date, email)

    def __deleteOldData__(self, data=[], user=None):
        """
            Recorre la lista de datos donde el usuario tiene una
            referencia o es la única referencia hacia los mismos.
            Si es la única referencia se elimina los datos,
            sino sólo se elimina la referencia.
        """
        for actividad in data:
            if actividad.usuario.count() > 1:
                actividad.usuario.remove(user)
            else:
                actividad.delete()

    def __cleanDataCVN__(self, user=None):
        """
            Elimina los datos introducidos previamente por el usuario.
            En caso que los datos pertenezcan a varios usuarios, se elimina
             sólo las referencias del usuario a los mismos.

            Variables:
            - user -> Usuario que está introduciendo un nuevo CVN.
        """
        # Actividad científica
        self.__deleteOldData__(Publicacion.objects.filter(usuario=user), user)
        self.__deleteOldData__(Congreso.objects.filter(usuario=user), user)
        self.__deleteOldData__(Proyecto.objects.filter(usuario=user), user)
        self.__deleteOldData__(Convenio.objects.filter(usuario=user), user)
        self.__deleteOldData__(TesisDoctoral.objects.filter(usuario=user),
                               user)

    def getXMLDate(self):
        date = self.tree.find('Version/VersionID/Date/Item').text.strip().split('-')
        return datetime.date(int(date[0]), int(date[1]), int(date[2]))

    def insertarXML(self, investigador=None):
        """
            Inserta los datos del CVN encontrados en el portal
            en la aplicación CVN

            Parametros:
            - investigador -> Usuario con el que se enlaza ambas BBDD.
        """
        dataPersonal = {}
        #fecha_cvn = None
        try:
            #tree = etree.parse(self.fileXML)
            #fecha_cvn = self.tree.find('Version/VersionID/Date/Item').text.strip()
            # Datos del Investigador
            dataInvestigador = self.tree.find('Agent')
                # /Identification/PersonalIdentification')
            dataPersonal = self.__parseDataIdentificationXML__(
                dataInvestigador.getchildren())
            search_data = searchDataUser(dataPersonal)
            if search_data:
                search_user = Usuario.objects.filter(**search_data)
                if not search_user:
                    #dataPersonal.update({'investigador': investigador})
                    user = Usuario.objects.create(**dataPersonal)
                else:
                    user = search_user[0]
                    # Se eliminan los datos previos del usuario
                    self.__cleanDataCVN__(user)
                # Introduce los datos de la actividad científica
                self.__parseActividadCientifica__(
                    user, self.tree.findall('CvnItem'))
            else:
                logger.warning("CVN sin datos personales: "
                               + str(self.fileXML))
        except IOError:
            if self.fileXML:
                logger.error("Fichero " + self.fileXML + u" no encontrado.")
            else:
                logger.warning(u'Se necesita un fichero '
                               u'para ejecutar este método')
        #return fecha_cvn

    def __parseDataIdentificationXML__(self, tree=None):
        """
            Obtiene los datos de identificación del usuario.
            Incluye datos:
                - Personales
                - Dirección
                - Contacto
            Variable:
            - tree: Subárbol cuyo nodo cabecera es "Agent" del cual cuelgan
                    todos los datos personales
        """
        dic = {}
        for element in tree:
            if element.tag == u'Identification' and element.getchildren():
                dic.update(self.__dataPersonalIdent__(
                    element.getchildren()[0].getchildren()))
            if element.tag == u'Address':
                dic.update(self.__dataAddress__(element.getchildren()))
            if element.tag == u'Contact':
                dic.update(self.__dataContact__(element.getchildren()))
        return dic

    def __dataPersonalIdent__(self, tree=[]):
        """
            Extrae un diccionario con los datos personales del usuario.

            Variable:
            - tree: Lista de los nodos con la información personal del usuario.
        """
        dic = {}
        for element in tree:
            if element.tag == u'OfficialId':
                dic[u'tipo_documento'] = u'' + element.getchildren()[0].tag
                dic[u'documento'] = u'' + formatNIF(
                    element.getchildren()[0].getchildren()[0].text.strip())
            elif element.tag == u'BirthRegion':
                dic[st.DIC_PERSONAL_DATA_XML[element.tag]] = unicode(
                    element.getchildren()[1].getchildren()[0].text.strip())
            else:
                # En caso de que sea un investigador extranjero
                # no tiene segundo apellido
                try:
                    dic[st.DIC_PERSONAL_DATA_XML[element.tag]] = unicode(
                        element.getchildren()[0].text.strip())
                except TypeError:
                    pass
        return dic

    def __dataAddress__(self, tree=[]):
        """
            Obtiene los datos de la dirección del usuario.
            Variables:
            - tree: Lista de los nodos con la información de la i
                dirección del usuario.
        """
        dic = {}
        for element in tree:
            if element.tag == u'Province' or element.tag == 'Region':
                dic[st.DIC_PERSONAL_DATA_XML[element.tag]] = unicode(
                    element.getchildren()[1].getchildren()[0].text.strip())
            else:
                dic[st.DIC_PERSONAL_DATA_XML[element.tag]] = unicode(
                    element.getchildren()[0].text.strip())
        return dic

    def __dataContact__(self, tree=[]):
        """
            Obtiene los datos de contacto del usuario.
            (telefonos y correo electronico)

            Variable:
            - tree: Lista de los nodos con la información de la
                contact del usuario.
        """
        dic = {}
        for element in tree:
            key = st.DIC_PERSONAL_DATA_XML[element.tag]
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
                    dic[telephone_key] = unicode(
                        children.getchildren()[0].text.strip())
            else:
                dic[key] = u'' + element.getchildren()[0].text.strip()
        return dic

    def __getAutores__(self, tree=[]):
        """
            Obtiene los autores participantes en la Actividad Científica

            Variable:
            - tree: Lista de los nodos con la información de los autores
        """
        lista_autores = ''
        for author in tree:
            auxAuthor = ''
            if author.find("GivenName/Item") is not None and\
               author.find("GivenName/Item").text is not None:
                auxAuthor = u'' + author.find("GivenName/Item").text.strip()
            if author.find("FirstFamilyName/Item") is not None and\
               author.find("FirstFamilyName/Item").text is not None:
                auxAuthor += u' ' + author.find(
                    "FirstFamilyName/Item").text.strip()
            # Algunas veces el campo está creado pero sin ningún valor.
            # El usuario introdujo un texto vacío.
            if author.find("SecondFamilyName/Item") is not None and\
               author.find("SecondFamilyName/Item").text is not None:
                auxAuthor += u' ' + author.find(
                    "SecondFamilyName/Item").text.strip()
            # Este elemento se crea siempre al exportar el PDF al XML
            if author.find("Signature/Item").text is not None:
                if auxAuthor:   # Si tiene datos, la firma va entre paréntesis
                    lista_autores += unicode(auxAuthor +
                                             ' (' +
                                             author.find("Signature/Item").text.strip() +
                                             '); ')
                else:         # El único dato de los autores es la firma
                    lista_autores += unicode(
                        author.find("Signature/Item").text.strip() + '; ')
            else:
                lista_autores += auxAuthor + '; '
        return lista_autores[:-2]

    def __getAmbito__(self, tree=[]):
        """
            Obtiene el ámbito de un Congreso, Proyecto o Convenio.

            Variable:
            - tree: Nodo que contiene los datos del ámbito.
        """
        data = {}
        if tree is not None:
            data['ambito'] = unicode(
                st.SCOPE[tree.find('Type/Item').text.strip()])
            # Campo supuestamente obligatorio en el Editor de FECYT,
            # pero algunos PDFs no lo tienen.
            # Posiblemente se generaron con alguna versión anterior
            # del editor.
            if data['ambito'] == u"Otros" and\
               (tree.find('Others/Item') is not None):
                data['otro_ambito'] = unicode(
                    tree.find('Others/Item').text.strip())
        return data

    def __getDuration__(self, code=""):
        """
            Obtiene la duración de un convenio.
            El código tiene el siguiente formato: "P<años>Y<meses>M<dias>D"

            Variable:
            - code: Cadena de texto con el código de duración del convenio
        """
        digit = ""
        data = {}
        for c in code[1:]:  # El primero carácter P se salta.
            if c.isdigit():
                digit += c
            else:
                if c == 'Y':
                    data['duracion_anyos'] = u'' + digit
                if c == 'M':
                    data['duracion_meses'] = u'' + digit
                if c == 'D':
                    data['duracion_dias'] = u'' + digit
                digit = ""
        return data

    def __saveData__(self, user=None, data={}, table_name=None):
        """
            Almacen de la actividad científica de un usuario en
            las tablas correspondientes.
            En caso de que exista ya dicho elemento almacenado en la tabla,
            simplemente se actualiza el campo usuario,
            añadiendo el nuevo usuario que se compartirá dicho mérito.

            Variables:
            - user: Usuario propietario de la actividad científica.
            - data: Datos a almacenar en la tabla correspondiente.
            - table: Tabla donde se va a almacenar o actualizar los datos
        """
        # Diccionario de búsqueda para comprobar
        # si existe ya el dato en la tabla
        search_data = searchDataProduccionCientifica(data)
        # Si devuelve un diccionario vacío, la búsqueda
        # devuelve todos los registros de la tabla
        if not search_data:
            search_data = {'pk': st.INVALID_SEARCH}
        table = get_model('cvn', table_name)
        try:
            reg = table.objects.get(**search_data)
            # Actualiza el registro con los nuevos datos
            table.objects.filter(pk=reg.id).update(**data)
        except ObjectDoesNotExist:
            # Se crea el nuevo registro en la tabla correspondiente
            reg = table.objects.create(**data)
        # Añade el usuario a la tabla
        reg.usuario.add(user)

    def __getDataPublicacion__(sefl, tree=[], tipo=""):
        """
            Obtiene los siguientes datos de la publicacion:
            - Página inicial y final
            - Volumen y número
            Retorna un diccionario con dichos valores.

            Variable:
            - tree: Lista de los nodos con la información
                de los autores participantes.
            - tipo: Indica el tipo de producción,
                   en caso de que se trate de un Artículo,
                   se almacena los datos del Volumen y el Número.
        """
        data = {}
        if tree is not None:
            if tree.find("Volume/Item") is not None:
                data['volumen'] = tree.find("Volume/Item").text.strip()
            if tree.find("Number/Item") is not None and\
               tree.find("Number/Item").text is not None:
                data['numero'] = tree.find("Number/Item").text.strip()
            #if tipo == u'Artículo':
            if tree.find("InitialPage/Item") is not None and\
               tree.find("InitialPage/Item").text is not None:
                data['pagina_inicial'] = tree.find(
                    "InitialPage/Item").text.strip()
                # checkPage(tree.find("InitialPage/Item").text)
            if tree.find("FinalPage/Item") is not None and\
               tree.find("FinalPage/Item").text is not None:
                data['pagina_final'] = tree.find("FinalPage/Item").text.strip()
        return data

    def __dataActividadCientificaPublicacion__(self, tree=[]):
        """
            Publicaciones, documentos científicos y técnicos

            Método que obtiene los datos de las publicaciones del usuario.
            Variable:
            - cvnpk: Identificador de la tabla de la Actividad Científica.
            - tree:  Elemento que contiene los datos de la publicación

            Return: Diccionario con los datos para la tabla "Publicación"
        """
        # Códigos de los atributos:
        # Artículos (35), Capítulos (148), Libros (112)
        data = {}
        try:
            tipo = st.ACTIVIDAD_CIENTIFICA_TIPO_PUBLICACION[
                tree.find('Subtype/SubType1/Item').text.strip()]
            data[u'tipo_de_produccion'] = u'' + tipo
            # Hay CVN que no tienen puesto el título
            if tree.find('Title/Name') is not None:
                data[u'titulo'] = unicode(
                    tree.find('Title/Name/Item').text.strip())
            if tree.find('Link/Title/Name') is not None and\
               tree.find('Link/Title/Name/Item').text is not None:
                data[u'nombre_publicacion'] = unicode(
                    tree.find('Link/Title/Name/Item').text.strip())
            data[u'autores'] = self.__getAutores__(tree.findall('Author'))
            data.update(self.__getDataPublicacion__(
                tree.find('Location'), tipo))
            # Fecha: Dia/Mes/Año
            if tree.find('Date/OnlyDate/DayMonthYear') is not None:
                data[u'fecha'] = unicode(
                    tree.find('Date/OnlyDate/DayMonthYear/Item').text.strip())
            # Fecha: Año
            elif tree.find('Date/OnlyDate/Year') is not None:
                data[u'fecha'] = unicode(formatDate(
                    tree.find('Date/OnlyDate/Year/Item').text.strip()))
            if tipo != u'Libro' and tree.find('ExternalPK') is not None:
                data[u'issn'] = unicode(tree.find(
                    'ExternalPK/Code/Item').text.strip())
        except KeyError:
            # El nodo no contiene ni artículos, ni capítulos ni libros.
            pass
        except AttributeError:
            # El nodo no tiene especificado el tipo de Item.
            pass
        return data

    def __dataActividadCientificaCongreso__(self, tree=[]):
        """
            Trabajos presentados en congresos nacionales o internacionales
            Variable:
            - Tree: Lista de nodos con la información sobre los
            "Trabajos presentados en congresos nacionales o internacionales."

            Return: Diccionario con los datos para la tabla "Congreso"
        """
        data = {}
        # Algunos trabajos no tienen puesto el nombre
        if tree.find('Title/Name') is not None:
            data[u'titulo'] = u'' + tree.find('Title/Name/Item').text.strip()
        for element in tree.findall('Link'):
            if element.find('CvnItemID/CodeCVNItem/Item').text.strip() == st.DATA_CONGRESO:
                if element.find('Title/Name') is not None and\
                   element.find('Title/Name/Item').text is not None:
                    data[u'nombre_del_congreso'] = unicode(
                        element.find('Title/Name/Item').text.strip())
                # Fecha de realización
                # Fecha: Dia/Mes/Año
                if element.find('Date/OnlyDate/DayMonthYear') is not None:
                    data[u'fecha_realizacion'] = unicode(
                        element.find(
                            'Date/OnlyDate/DayMonthYear/Item').text.strip())
                # Fecha: Año
                elif element.find('Date/OnlyDate/Year') is not None:
                    data[u'fecha_realizacion'] = unicode(formatDate(
                        element.find('Date/OnlyDate/Year/Item').text.strip()))
                # Fecha de finalización
                # Fecha: Dia/Mes/Año
                if element.find('Date/EndDate/DayMonthYear') is not None:
                    data[u'fecha_finalizacion'] = unicode(element.find(
                        'Date/EndDate/DayMonthYear/Item').text.strip())
                # Fecha: Año
                elif element.find('Date/EndDate/Year') is not None:
                    data[u'fecha_finalizacion'] = unicode(formatDate(
                        element.find('Date/EndDate/Year/Item').text.strip()))
                if element.find('Place/City') is not None:
                    data[u'ciudad_de_realizacion'] = unicode(element.find(
                        'Place/City/Item').text.strip())
                # Ámbito
                data.update(self.__getAmbito__(element.find('Scope')))

        data[u'autores'] = self.__getAutores__(tree.findall('Author'))
        return data

    def __dataExperienciaCientifica__(self, tree=[], tipo=""):
        """
            Convenios y Proyectos de I+D+i

            Obtiene los datos de tanto de la "participación en contratos,
            convenios o proyectos de I+D+i no competitivos con
            Administraciones o entidades públicas o privadas"
            como de "participación en proyectos de I+D+i financiados en
            convocatorias competitivas de Administraciones o entidades
            públicas y privadas".

            Variable:
            - tree: Lista de nodos con la información sobre los convenios.
            - tipo: Indica si se trata de un Convenio o un Proyecto

            Return: Diccionario con los datos para la tabla "Publicación"
        """
        data = {}
        # Hay CVN que no tienen puesta la denominación del proyecto
        if tree.find('Title/Name') is not None:
            data[u'denominacion_del_proyecto'] = unicode(tree.find(
                'Title/Name/Item').text.strip())

        # Posibles nodos donde se almacena la fecha
        if tree.find('Date/StartDate'):
            nodo = "StartDate"
        else:
            nodo = "OnlyDate"
        # Según se trate de un convenio o proyecto la fecha inicial
        # cuelga de un nodo diferente
        #~ if st.MODEL_TABLE[tipo] == Convenio:
            #~ nodo = "OnlyDate"

        # Fecha de inicio Convenios y Proyectos
        # Fecha: Dia/Mes/Año
        if tree.find('Date/' + nodo + '/DayMonthYear') is not None:
            data[u'fecha_de_inicio'] = unicode(tree.find(
                'Date/' + nodo + '/DayMonthYear/Item').text.strip())
        # Fecha: Año
        elif tree.find('Date/' + nodo + '/Year') is not None:
            data[u'fecha_de_inicio'] = unicode(formatDate(
                tree.find('Date/' + nodo + '/Year/Item').text.strip()))

        # Fecha final Proyectos
        if st.MODEL_TABLE[tipo] == u'Proyecto':
            if tree.find('Date/EndDate/DayMonthYear') is not None and\
               tree.find('Date/EndDate/DayMonthYear/Item').text is not None:
                data[u'fecha_de_fin'] = unicode(tree.find(
                    'Date/EndDate/DayMonthYear/Item').text.strip())
            elif tree.find('Date/EndDate/Year') is not None and\
                 tree.find('Date/EndDate/Year/Item').text is not None:
                data[u'fecha_de_fin'] = unicode(formatDate(tree.find(
                    'Date/EndDate/Year/Item').text.strip()))

        # La duración del proyecto viene codificada en el formato:
        # P <num_years> Y <num_months> M <num_days> D
        if tree.find('Date/Duration') is not None and\
           tree.find('Date/Duration/Item').text is not None:
            duration_code = u'' + tree.find('Date/Duration/Item').text.strip()
            data.update(self.__getDuration__(duration_code))
            # TODO Calcular fecha final partiendo de la duración
            # si se trata de un Convenio

        data[u'autores'] = self.__getAutores__(tree.findall('Author'))

        # Dimensión Económica
        for element in tree.findall('EconomicDimension'):
            economic_code = element.find('Value').attrib['code']
            data[st.ECONOMIC_DIMENSION[economic_code]] = unicode(element.find(
                'Value/Item').text.strip())
        if tree.find('ExternalPK/Code') is not None:
            data[u'cod_segun_financiadora'] = unicode(tree.find(
                'ExternalPK/Code/Item').text.strip())

        # Ámbito
        data.update(self.__getAmbito__(tree.find('Scope')))
        return data

    def __dataActividadDocente__(self, tree=[]):
        """
            Dirección de tesis doctorales y/o proyectos fin de carrera

            Obtiene la Actividad docente de un usuario.
            Sección del Editor "Dirección de tesis doctorales y/o
                proyectos fin de carrera".

            Variable:
            - tree: Lista de nodos con la información necesaria para
                obtener los datos de la tesis

            Return: Diccionario con los datos para insertar en la tabla
        """
        data = {}
        # Comprueba si la actividad docente se trata de una tesis
        try:
            if tree.find('Subtype/SubType1/Item').text.strip() == st.DATA_TESIS:
                data[u'titulo'] = unicode(tree.find(
                    'Title/Name/Item').text.strip())
                data[u'universidad_que_titula'] = unicode(tree.find(
                    'Entity/EntityName/Item').text.strip())
                data[u'autor'] = self.__getAutores__(tree.findall('Author'))
                data[u'codirector'] = self.__getAutores__(
                    tree.findall('Link/Author'))
                data[u'fecha_de_lectura'] = unicode(tree.find(
                    'Date/OnlyDate/DayMonthYear/Item').text.strip())
        except AttributeError:
            # No tiene elemento tipo: 'Subtype/SubType1/Item'
            pass
        return data

    def __parseActividadCientifica__(self, user=None, cvnItems=[]):
        """
            Obtiene los datos de la Actividad científica de un usuario.
            Recorre el XML buscando aquellos nodos 'CVNItem' cuyo
            'CvnItemID/CVNPK' se engloban dentro de '060.XXX.XXX.XXX'.
            Variable:
            - user: Usuario del CVN
            - cvnItems: Lista de los nodos con la información de los
                méritos almacenada en el CVN.
        """
        # Recorre los méritos introducidos en el CVN por el investigador
        for element in cvnItems:
            data = {}
            cvn_key = element.find('CvnItemID/CVNPK/Item').text.strip()
            # Actividad docente (Paso 4 Editor FECYT)
            if cvn_key == u"030.040.000.000":
                data = self.__dataActividadDocente__(element)
            # Experiencia científica y tecnológica (Paso 5 Editor FECYT)
            if cvn_key == u"050.020.020.000" or cvn_key == u"050.020.010.000":
                data = self.__dataExperienciaCientifica__(element, cvn_key)
            # Actividad científica y tecnológica (Paso 6 Editor FECYT)
            # Publicación, documentos científicos y técnicos
            if cvn_key == u"060.010.010.000":
                data = self.__dataActividadCientificaPublicacion__(element)
            # Trabajos presentados en congresos nacionales o internacionales.
            if cvn_key == u"060.010.020.000":
                data = self.__dataActividadCientificaCongreso__(element)
            # Almacena los datos
            if data:
                self.__saveData__(user, data, st.MODEL_TABLE[cvn_key])


def insert_pdf_to_bbdd_if_not_exists(nif="", investCVN=None):
    """
        Inserta el CVN en la BBDD si el usuario no lo tiene
         insertado previamente.

        Variables:
        - nif = NIF/NIE del usuario
        - investCVN  = Registro de la tabla GrupoinvestInvestcvn de ViinV
    """
    if not Usuario.objects.filter(documento__icontains=nif):
        if not investCVN.xmlfile:
            handlerCVN = UtilidadesCVNtoXML(filePDF=investCVN.cvnfile)
            xmlFecyt = handlerCVN.getXML()
            # Si el CVN tiene formato FECYT y
            # el usuario es el propietario se actualiza
            if xmlFecyt and \
               handlerCVN.checkCVNOwner(investCVN.investigador, xmlFecyt):
                investCVN.xmlfile.save(investCVN.cvnfile.name.replace('pdf', 'xml'), ContentFile(xmlFecyt))
        utils = UtilidadesXMLtoBBDD(fileXML=investCVN.xmlfile)
        utils.insertarXML(investCVN.investigador)
        investCVN.fecha_cvn = utils.getXMLDate()
        investCVN.save()
