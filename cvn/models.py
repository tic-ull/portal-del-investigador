# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.utils import noneToZero
from django.contrib.auth.models import User
from django.db import models
from managers import (PublicacionManager, CongresoManager, ProyectoManager,
                      ConvenioManager, TesisDoctoralManager)
from django.conf import settings as st
from django.core.files.move import file_move_safe
from lxml import etree
import base64
import os
import datetime
import logging
import suds
import time
import sys


logger = logging.getLogger(__name__)


def get_produccion_from_fecyt_code(cvn_key):
    if not cvn_key in stCVN.FECYT_CODE:
        return None
    return getattr(sys.modules[__name__], stCVN.FECYT_CODE[cvn_key])


class FECYT(models.Model):

    @staticmethod
    def getXML(filePDF):
        try:
            dataPDF = base64.encodestring(filePDF.read())
        except IOError:
            logger.error(u'ERROR: No existe el fichero o directorio: %s' % (
                filePDF.name))
            return False

        # Web Service - FECYT
        clientWS = suds.client.Client(stCVN.URL_WS)
        WSResponse = False
        while not WSResponse:
            try:
                resultXML = clientWS.service.cvnPdf2Xml(
                    stCVN.USER_WS, stCVN.PASSWD_WS, dataPDF)
                WSResponse = True
            except:
                logger.warning(u'WARNING: No hay respuesta del WS \
                    de la FECYT para el fichero %s' % (filePDF.name))
                time.sleep(5)

        # Format CVN-XML of FECYT
        if resultXML.errorCode == 0:
            return (base64.decodestring(resultXML.cvnXml), 0)
        return (False, resultXML.errorCode)

    class Meta:
        managed = False


class CVN(models.Model):
    cvn_file = models.FileField(upload_to=stCVN.PDF_ROOT)
    xml_file = models.FileField(upload_to=stCVN.XML_ROOT)
    fecha_cvn = models.DateField()
    created_at = models.DateTimeField(u'Creado', auto_now_add=True)
    updated_at = models.DateTimeField(u'Actualizado', auto_now=True)

    def __unicode__(self):
        return u'%s con fecha %s' % (self.cvn_file, self.fecha_cvn)

    @staticmethod
    def get_nif_from_xml(xml):
        nif = ''
        xml_tree = etree.XML(xml)
        id_node = xml_tree.find(
            'Agent/Identification/PersonalIdentification/OfficialId')
        nif_node = id_node.find('DNI/Item')
        if nif_node is None:
            nif_node = id_node.find('NIE/Item')

        if nif_node is not None:
            nif = nif_node.text.strip()

        return nif

    @classmethod
    def can_user_upload_cvn(cls, user, xml):
        nif = cls.get_nif_from_xml(xml)
        if (user.has_perm('can_upload_other_users_cvn') or
           nif.upper() == user.profile.documento.upper()):
            return True
        return False

    @staticmethod
    def get_date_from_xml(xml):
        treeXML = etree.XML(xml)
        date = treeXML.find(
            'Version/VersionID/Date/Item').text.strip().split('-')
        return datetime.date(int(date[0]), int(date[1]), int(date[2]))

    def remove(self):
        # Removes data related to CVN that is not on the CVN class.
        self._backup_pdf()
        if self.xml_file:
            self.xml_file.delete()      # Remove pdf file
        self._remove_producciones()     # Removed info related to pdf
                                        # from all databases

    def _backup_pdf(self):
        cvn_path = os.path.join(st.MEDIA_ROOT, self.cvn_file.name)
        old_path = os.path.join(st.MEDIA_ROOT, stCVN.OLD_PDF_ROOT)
        new_file_name = self.cvn_file.name.split('/')[-1].replace(
            u'.pdf', u'-' + str(
                self.updated_at.strftime('%Y-%m-%d')
            ) + u'.pdf')
        old_cvn_file = os.path.join(old_path, new_file_name)
        if not os.path.isdir(old_path):
            os.makedirs(old_path)
        file_move_safe(cvn_path, old_cvn_file, allow_overwrite=True)

    def insert_xml(self):
        try:
            self.xml_file.seek(0)
            CVNItems = etree.parse(self.xml_file).findall('CvnItem')
            self._parse_producciones(CVNItems)
        except IOError:
            if self.xml_file:
                logger.error(u'ERROR: No existe el fichero %s' % (
                    self.xml_file.name))
            else:
                logger.warning(u'WARNING: Se requiere de un fichero CVN-XML')

    def _remove_producciones(self):
        Publicacion.objects.removeByUserProfile(self.user_profile)
        Congreso.objects.removeByUserProfile(self.user_profile)
        Proyecto.objects.removeByUserProfile(self.user_profile)
        Convenio.objects.removeByUserProfile(self.user_profile)
        TesisDoctoral.objects.removeByUserProfile(self.user_profile)

    def _parse_producciones(self, CVNItems):
        for CVNItem in CVNItems:
            #data = {}
            cvn_key = CVNItem.find('CvnItemID/CVNPK/Item').text.strip()
            produccion = get_produccion_from_fecyt_code(cvn_key)
            if produccion is None:
                continue
            #import pdb; pdb.set_trace()
            produccion.objects.newInstance(CVNItem, self.user_profile)

            '''if stCVN.FECYT_CODE[cvn_key] == 'TesisDoctoral':
                data = self._dataTeaching(CVNItem)
            if stCVN.FECYT_CODE[cvn_key] in ['Proyecto', 'Convenio']:
                data = self._dataScientificExperience(CVNItem, cvn_key)
            if stCVN.MODEL_TABLE[cvn_key] == 'Publicacion':
                data = self._dataPublications(CVNItem)
                if data and 'tipo_de_produccion' in data:
                    if data['tipo_de_produccion'] == 'Articulo':
                        self._saveData(data, 'Articulo')
                    if data['tipo_de_produccion'] == 'Libro':
                        self._saveData(data, 'Libro')
                    if data['tipo_de_produccion'] == 'Capitulo de Libro':
                        self._saveData(data, 'Capitulo')
                    continue
            if stCVN.MODEL_TABLE[cvn_key] == 'Congreso':
                data = self._dataCongress(CVNItem)
            if data:
                self._saveData(data, stCVN.MODEL_TABLE[cvn_key])
            '''

    def _dataTeaching(self, treeXML):
        dataCVN = {}
        try:
            if treeXML.find(
                'Subtype/SubType1/Item'
            ).text.strip() == stCVN.DATA_TESIS:
                dataCVN[u'titulo'] = unicode(treeXML.find(
                    'Title/Name/Item').text.strip())
                dataCVN[u'universidad_que_titula'] = unicode(treeXML.find(
                    'Entity/EntityName/Item').text.strip())
                dataCVN[u'autor'] = self._getAuthors(
                    treeXML.findall('Author'))
                dataCVN[u'codirector'] = self._getAuthors(
                    treeXML.findall('Link/Author'))
                dataCVN[u'fecha_de_lectura'] = unicode(treeXML.find(
                    'Date/OnlyDate/DayMonthYear/Item').text.strip())
        except AttributeError:
            pass
        return dataCVN

    '''def _dataScientificExperience(self, treeXML, typeItem):
        dataCVN = {}
        # Demonicación del Proyecto
        if treeXML.find('Title/Name'):
            dataCVN[u'denominacion_del_proyecto'] = unicode(treeXML.find(
                'Title/Name/Item').text.strip())
        # Posibles nodos Fecha
        if treeXML.find('Date/StartDate'):
            node = 'StartDate'
        else:
            node = 'OnlyDate'
        # Fecha de Inicio: Día/Mes/Año
        if treeXML.find('Date/' + node + '/DayMonthYear'):
            dataCVN[u'fecha_de_inicio'] = unicode(treeXML.find(
                'Date/' + node + '/DayMonthYear/Item').text.strip())
        # Fecha de Inicio: Año
        elif treeXML.find('Date/' + node + '/Year'):
            dataCVN[u'fecha_de_inicio'] = unicode(treeXML.find(
                'Date/' + node + '/Year/Item').text.strip() + '-1-1')
        # Fecha de Finalización
        if stCVN.MODEL_TABLE[typeItem] == u'Proyecto':
            if (treeXML.find('Date/EndDate/DayMonthYear') and
               treeXML.find('Date/EndDate/DayMonthYear/Item').text):
                dataCVN[u'fecha_de_fin'] = unicode(treeXML.find(
                    'Date/EndDate/DayMonthYear/Item').text.strip())
            elif (treeXML.find('Date/EndDate/Year') and
                  treeXML.find('Date/EndDate/Year/Item').text):
                dataCVN[u'fecha_de_fin'] = unicode(treeXML.find(
                    'Date/EndDate/Year/Item').text.strip() + '-1-1')
        # Duración: P <num_years> Y <num_months> M <num_days> D
        if (treeXML.find('Date/Duration') and
           treeXML.find('Date/Duration/Item').text):
            duration = unicode(treeXML.find('Date/Duration/Item').text.strip())
            dataCVN.update(self._getDuration(duration))
        # Autores
        dataCVN[u'autores'] = self._getAuthors(treeXML.findall('Author'))
        # Dimensión Económica
        for itemXML in treeXML.findall('EconomicDimension'):
            economic = itemXML.find('Value').attrib['code']
            dataCVN[stCVN.ECONOMIC_DIMENSION[economic]] = unicode(itemXML.find(
                'Value/Item').text.strip())
        if treeXML.find('ExternalPK/Code'):
            dataCVN[u'cod_segun_financiadora'] = unicode(treeXML.find(
                'ExternalPK/Code/Item').text.strip())
        # Ámbito
        dataCVN.update(self._getScope(treeXML.find('Scope')))
        return dataCVN
    '''

    def _dataPublications(self, treeXML):
        # Artículos (35), Capítulos (148), Libros (112)
        dataCVN = {}
        try:
            typePublication = stCVN.ACTIVIDAD_CIENTIFICA_TIPO_PUBLICACION[
                treeXML.find('Subtype/SubType1/Item').text.strip()]
            dataCVN[u'tipo_de_produccion'] = typePublication
            if treeXML.find('Title/Name'):
                dataCVN[u'titulo'] = unicode(treeXML.find(
                    'Title/Name/Item').text.strip())
            if (treeXML.find('Link/Title/Name') and
               treeXML.find('Link/Title/Name/Item').text):
                dataCVN[u'nombre_publicacion'] = unicode(treeXML.find(
                    'Link/Title/Name/Item').text.strip())
            dataCVN[u'autores'] = self._getAuthors(treeXML.findall(
                'Author'))
            dataCVN.update(self._getDataPublication(treeXML.find('Location')))
            # Fecha: Dia/Mes/Año
            if treeXML.find('Date/OnlyDate/DayMonthYear'):
                dataCVN[u'fecha'] = unicode(treeXML.find(
                    'Date/OnlyDate/DayMonthYear/Item').text.strip())
            # Fecha: Año
            elif treeXML.find('Date/OnlyDate/Year'):
                dataCVN[u'fecha'] = unicode(treeXML.find(
                    'Date/OnlyDate/Year/Item').text.strip() + '-1-1')
            if typePublication != u'Libro' and treeXML.find('ExternalPK'):
                dataCVN[u'issn'] = unicode(treeXML.find(
                    'ExternalPK/Code/Item').text.strip())
        except KeyError:
            pass
        except AttributeError:
            pass
        return dataCVN

    def _getDataPublication(self, treeXML):
        data = {}
        if treeXML:
            volume = treeXML.find('Volume/Item')
            if volume is not None and volume.text is not None:
                data['volumen'] = volume.text.strip()
            number = treeXML.find('Number/Item')
            if number is not None and number.text is not None:
                data['numero'] = number.text.strip()
            page = treeXML.find('InitialPage/Item')
            if page is not None and page.text is not None:
                data['pagina_inicial'] = page.text.strip()
            page = treeXML.find('FinalPage/Item')
            if page is not None and page.text is not None:
                data['pagina_final'] = page.text.strip()
        return data


    def _getDataSearch(self, dataCVN=None):
        itemCVN = {}
        if 'denominacion_del_proyecto' in dataCVN:
            itemCVN['denominacion_del_proyecto__iexact'] = (
                dataCVN['denominacion_del_proyecto'])
        elif 'titulo' in dataCVN:
            itemCVN['titulo__iexact'] = dataCVN['titulo']
        return itemCVN

    def _dataCongress(self, treeXML):
        dataCVN = {}
        if treeXML.find('Title/Name'):
            dataCVN[u'titulo'] = unicode(treeXML.find(
                'Title/Name/Item').text.strip())
        for itemXML in treeXML.findall('Link'):
            if itemXML.find(
                'CvnItemID/CodeCVNItem/Item'
            ).text.strip() == stCVN.DATA_CONGRESO:
                if (itemXML.find('Title/Name') and
                   itemXML.find('Title/Name/Item').text):
                    dataCVN[u'nombre_del_congreso'] = unicode(itemXML.find(
                        'Title/Name/Item').text.strip())
                # Fecha: Dia/Mes/Año
                if itemXML.find('Date/OnlyDate/DayMonthYear'):
                    dataCVN[u'fecha_realizacion'] = unicode(itemXML.find(
                        'Date/OnlyDate/DayMonthYear/Item').text.strip())
                # Fecha: Año
                elif itemXML.find('Date/OnlyDate/Year'):
                    dataCVN[u'fecha_realizacion'] = unicode(
                        itemXML.find(
                            'Date/OnlyDate/Year/Item'
                        ).text.strip() + '-1-1')
                # Fecha: Dia/Mes/Año
                if itemXML.find('Date/EndDate/DayMonthYear'):
                    dataCVN[u'fecha_finalizacion'] = unicode(itemXML.find(
                        'Date/EndDate/DayMonthYear/Item').text.strip())
                # Fecha: Año
                elif itemXML.find('Date/EndDate/Year'):
                    dataCVN[u'fecha_finalizacion'] = unicode(
                        itemXML.find(
                            'Date/EndDate/Year/Item'
                        ).text.strip() + '-1-1')
                if itemXML.find('Place/City'):
                    dataCVN[u'ciudad_de_realizacion'] = unicode(itemXML.find(
                        'Place/City/Item').text.strip())
                # Ámbito
                dataCVN.update(self._getScope(itemXML.find('Scope')))
        dataCVN[u'autores'] = self._getAuthors(treeXML.findall('Author'))
        return dataCVN


class UserProfile(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#IDENTIFICACION
    """
    user = models.OneToOneField(User, related_name='profile')
    cvn = models.OneToOneField(CVN, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name='user_profile')
    documento = models.CharField(u'Documento', max_length=20,
                                 blank=True, null=True, unique=True)
    rrhh_code = models.CharField(u'Código persona', max_length=20,
                                 blank=True, null=True, unique=True)

    def __unicode__(self):
        return self.user.username


class Publicacion(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#ACTIVIDAD_CIENTIFICA
    """
    #FECYT_CODE = stCVN.FECYT_CODE['Publicacion']
    objects = PublicacionManager()
    # Campo recomendado
    titulo = models.TextField(u'Título de la publicación',
                              blank=True, null=True)

    # Una publicación puede pertenecer a varios usuarios.
    user_profile = models.ManyToManyField(UserProfile, blank=True, null=True)

    # Campos recomendados
    tipo_de_produccion = models.CharField(u'Tipo de producción',
                                          max_length=50, blank=True, null=True)
    fecha = models.DateField(u'Fecha', blank=True, null=True)

    tipo_de_soporte = models.CharField(u'Tipo de soporte',
                                       max_length=1000, blank=True, null=True)
    # Publicaciones con nombre de hasta 1400 caracteres
    nombre_publicacion = models.TextField(u'Nombre de la publicación',
                                          blank=True, null=True)
    editorial = models.CharField(u'Editorial',
                                 max_length=500, blank=True, null=True)

    # Volumen
    volumen = models.CharField(u'Volumen',
                               max_length=100, blank=True, null=True)
    numero = models.CharField(u'Número',
                              max_length=100, blank=True, null=True)
    pagina_inicial = models.CharField(u'Página Inicial',
                                      max_length=100, blank=True, null=True)
    pagina_final = models.CharField(u'Página Final',
                                    max_length=100, blank=True, null=True)

    autores = models.TextField(u'Autores', blank=True, null=True)

    # Otros campos
    posicion_sobre_total = models.IntegerField(u'Posición sobre total',
                                               blank=True, null=True)
    en_calidad_de = models.CharField(u'En calidad de',
                                     max_length=500, blank=True, null=True)

    isbn = models.CharField(u'ISBN', max_length=150, blank=True, null=True)
    issn = models.CharField(u'ISSN', max_length=150, blank=True, null=True)

    deposito_legal = models.CharField(u'Depósito legal',
                                      max_length=150, blank=True, null=True)
    url = models.URLField(u'URL', max_length=500, blank=True, null=True)
    coleccion = models.CharField(u'Colección',
                                 max_length=150, blank=True, null=True)

    ciudad = models.CharField(u'Ciudad de la titulación',
                              max_length=500,  blank=True, null=True)
    pais = models.CharField(u'País de la titulación',
                            max_length=500, blank=True, null=True)
    comunidad_or_region = models.CharField(u'Autónoma/Reg. de trabajo',
                                           max_length=500,
                                           blank=True, null=True)

    # Índice de impacto
    fuente_de_impacto = models.CharField(u'Fuente de impacto',
                                         max_length=500, blank=True, null=True)
    categoria = models.CharField(u'Categoría',
                                 max_length=500, blank=True, null=True)
    indice_de_impacto = models.CharField(u'Índice de impacto',
                                         max_length=500, blank=True, null=True)
    posicion = models.IntegerField(u'Posicion', blank=True, null=True)
    num_revistas = models.IntegerField(u'Número de revistas en la categoría',
                                       blank=True, null=True)
    revista_25 = models.CharField(u'Revista dentro del 25%',
                                  max_length=50, blank=True, null=True)

    # Citas
    fuente_de_citas = models.CharField(u'Fuente de citas',
                                       max_length=500, blank=True, null=True)
    citas = models.CharField(u'Citas', max_length=500, blank=True, null=True)

    publicacion_relevante = models.CharField(u'Publicación relevante',
                                             max_length=50,
                                             blank=True, null=True)
    resenyas_en_revista = models.CharField(u'Reseñas en revistas',
                                           max_length=500,
                                           blank=True, null=True)

    # Traducciones
    # NOTE: Campo de autocompletado. Desde este control se permite
    # seleccionar varias titulaciones de la norma.
    filtro = models.CharField(u'Filtro', max_length=500, blank=True, null=True)
    resultados_destacados = models.TextField(u'Resultados destacados',
                                             blank=True, null=True)

    created_at = models.DateTimeField(u'Creado', auto_now_add=True)
    updated_at = models.DateTimeField(u'Actualizado', auto_now=True)

    def __unicode__(self):
        return "%s %s" % (self.tipo_de_produccion, self.titulo)

    class Meta:
        verbose_name_plural = u'Publicaciones'
        ordering = ['-fecha', 'titulo']


class Articulo(Publicacion):

    class Meta:
        verbose_name_plural = u'Artículos'


class Libro(Publicacion):

    class Meta:
        verbose_name_plural = u'Libros'


class Capitulo(Publicacion):

    class Meta:
        verbose_name_plural = u'Capítulos de Libros'


class Congreso(models.Model):
    """
        # https://cvn.fecyt.es/editor/cvn.html?locale=spa#ACTIVIDAD_CIENTIFICA
    """
    objects = CongresoManager()
    user_profile = models.ManyToManyField(UserProfile, blank=True, null=True)

    # Campos recomendados
    titulo = models.TextField(u'Título', blank=True, null=True)
    fecha_realizacion = models.DateField(u'Fecha de realización',
                                         blank=True, null=True)
    fecha_finalizacion = models.DateField(u'Fecha de finalización',
                                          blank=True, null=True)

    nombre_del_congreso = models.TextField(u'Nombre del congreso',
                                           blank=True, null=True)
    ciudad_de_realizacion = models.CharField(u'Ciudad de realización',
                                             max_length=500,
                                             blank=True, null=True)
    pais_de_realizacion = models.CharField(u'País de realización',
                                           max_length=500,
                                           blank=True, null=True)
    comunidad_or_region_realizacion = models.CharField(
        u'Comunidad/Región de realizacion',
        max_length=500, blank=True, null=True
    )

    entidad_organizadora = models.CharField(u'Entidad organizadora',
                                            max_length=250,
                                            blank=True, null=True)
    ciudad = models.CharField(u'Ciudad', max_length=500, blank=True, null=True)
    pais = models.CharField(u'País', max_length=500, blank=True, null=True)
    comunidad_or_region = models.CharField(u'Comunidad autónoma/Región',
                                           max_length=500,
                                           blank=True, null=True)

    autores = models.TextField(u'Autores', blank=True, null=True)

    titulo_publicacion = models.CharField(u'Título de la publicación',
                                          max_length=250,
                                          blank=True, null=True)

    tipo_evento = models.CharField(u'Tipo evento',
                                   max_length=50, blank=True, null=True)
    tipo = models.CharField(u'Tipo', max_length=250, blank=True, null=True)
    fecha = models.DateField(u'Fecha', blank=True, null=True)
    nombre_de_publicacion = models.CharField(u'Nombre de la publicación',
                                             max_length=250,
                                             blank=True, null=True)
    comite_admision_externa = models.CharField(
        u'Con comité de admisión externa',
        max_length=250, blank=True, null=True
    )

    ambito = models.CharField(u'Ámbito del congreso',
                              max_length=50, blank=True, null=True)
    otro_ambito = models.CharField(u'Otro ámbito',
                                   max_length=250, blank=True, null=True)

    tipo_de_participacion = models.CharField(u'Tipo de participación',
                                             max_length=250,
                                             blank=True, null=True)
    intervencion_por = models.CharField(u'Intevención por',
                                        max_length=250,
                                        blank=True, null=True)

    volumen = models.CharField(u'Volumen',
                               max_length=100, blank=True, null=True)
    numero = models.CharField(u'Número', max_length=100, blank=True, null=True)
    pagina_inicial = models.CharField(u'Página Inicial',
                                      max_length=100, blank=True, null=True)
    pagina_final = models.CharField(u'Página Final',
                                    max_length=100, blank=True, null=True)

    editorial = models.CharField(u'Editorial',
                                 max_length=500, blank=True, null=True)

    isbn = models.CharField(u'ISBN', max_length=150, blank=True, null=True)
    issn = models.CharField(u'ISSN', max_length=150, blank=True, null=True)

    deposito_legal = models.CharField(u'Depósito legal',
                                      max_length=150, blank=True, null=True)
    publicacion_acta_congreso = models.CharField(
        u'Publicación en acta congreso',
        max_length=100, blank=True, null=True
    )

    url = models.URLField(u'Url', max_length=500, blank=True, null=True)

    pais = models.CharField(u'País', max_length=500, blank=True, null=True)
    comunidad_or_region = models.CharField(u'Comunidad Autónoma/Región',
                                           max_length=500,
                                           blank=True, null=True)

    created_at = models.DateTimeField(u'Creado', auto_now_add=True)
    updated_at = models.DateTimeField(u'Actualizado', auto_now=True)

    def __unicode__(self):
        return "%s" % (self.titulo)

    class Meta:
        verbose_name_plural = u'Congresos'
        ordering = ['-fecha_realizacion', 'titulo']


################### Experiencia científica y tecnológica ####################
class Proyecto(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale\
        =spa#EXPERIENCIA_CIENTIFICA_dataGridProyIDIComp
    """
    objects = ProyectoManager()
    user_profile = models.ManyToManyField(UserProfile, blank=True, null=True)

    # Campos recomendados
    denominacion_del_proyecto = models.CharField('Denominación del proyecto',
                                                 max_length=1000,
                                                 blank=True, null=True)
    numero_de_investigadores = models.IntegerField(
        u'Número de investigadores/as',
        blank=True, null=True
    )

    ### Investigadores responsables ###
    autores = models.TextField(u'Autores', blank=True, null=True)

    entidad_de_realizacion = models.CharField(u'Entidad de realización',
                                              max_length=500,
                                              blank=True, null=True)

    ciudad_del_proyecto = models.CharField(u'Ciudad del trabajo',
                                           max_length=500,
                                           blank=True, null=True)
    pais_del_proyecto = models.CharField(u'País del trabajo',
                                         max_length=500, blank=True, null=True)
    comunidad_or_region_proyecto = models.CharField(
        u'Autónoma/Reg. del trabajo',
        max_length=500, blank=True, null=True)

    ### Entidades financiadoras ###
    #FIXME En el editor de la FECYT se pueden añadir múltiples
    # entidades financiadoras
    entidad_financiadora = models.CharField(u'Entidad financiadora',
                                            max_length=500,
                                            blank=True, null=True)
    tipo_de_entidad = models.CharField(u'Tipo de entidad',
                                       max_length=500, blank=True, null=True)

    ciudad_de_la_entidad = models.CharField(u'Ciudad del trabajo',
                                            max_length=500,
                                            blank=True, null=True)
    pais_de_la_entidad = models.CharField(u'País del trabajo',
                                          max_length=500,
                                          blank=True, null=True)
    comunidad_or_region_entidad = models.CharField(
        u'Autónoma/Reg. del trabajo',
        max_length=500, blank=True, null=True
    )

    fecha_de_inicio = models.DateField(u'Fecha de inicio',
                                       blank=True, null=True)
    fecha_de_fin = models.DateField(u'Fecha de finalización',
                                    blank=True, null=True)

    cuantia_total = models.DecimalField(u'Cuantía',
                                        max_digits=19, decimal_places=2,
                                        blank=True, null=True)

    # Más campos
    duracion_anyos = models.IntegerField(u'Duración en años',
                                         blank=True, null=True)
    duracion_meses = models.IntegerField(u'Duración en meses',
                                         blank=True, null=True)
    duracion_dias = models.IntegerField(u'Duración en días',
                                        blank=True, null=True)

    palabras_clave = models.CharField(u'Describir con palabras clave',
                                      max_length=250, blank=True, null=True)

    modalidad_del_proyecto = models.CharField(u'Modalidad del proyecto',
                                              max_length=500,
                                              blank=True, null=True)

    ambito = models.CharField(u'Ámbito del proyecto',
                              max_length=50, blank=True, null=True)
    otro_ambito = models.CharField(u'Otro ámbito',
                                   max_length=250, blank=True, null=True)

    numero_personas_anyo = models.IntegerField(u'Número personas/año',
                                               blank=True, null=True)
    calidad_participacion = models.CharField(u'Calidad en que ha participado',
                                             max_length=500,
                                             blank=True, null=True)
    tipo_participacion = models.CharField(u'Tipo de participación',
                                          max_length=500,
                                          blank=True, null=True)
    nombre_del_programa = models.CharField(u'Nombre del programa',
                                           max_length=500,
                                           blank=True, null=True)

    cod_segun_financiadora = models.CharField(u'Código según financiadora',
                                              max_length=150,
                                              blank=True, null=True)
    cuantia_subproyecto = models.DecimalField(u'Cuantía subproyecto',
                                              max_digits=19, decimal_places=2,
                                              blank=True, null=True)
    porcentaje_en_subvencion = models.DecimalField(u'Porcentaje en subvención',
                                                   max_digits=19,
                                                   decimal_places=2,
                                                   blank=True, null=True)
    porcentaje_en_credito = models.DecimalField(u'Porcentaje en crédito',
                                                max_digits=19,
                                                decimal_places=2,
                                                blank=True, null=True)
    porcentaje_mixto = models.DecimalField(u'Porcentaje mixto',
                                           max_digits=19, decimal_places=2,
                                           blank=True, null=True)
    resultados_mas_relevantes = models.CharField(u'Resultados más relevantes',
                                                 max_length=1024,
                                                 blank=True, null=True)
    dedicacion = models.CharField(u'Dedicación',
                                  max_length=16, blank=True, null=True)
    palabras_clave_dedicacion = models.CharField(u'Palabras clave dedicación',
                                                 max_length=500,
                                                 blank=True, null=True)

    ### Entidades participantes ###
    #FIXME En el editor de la FECYT se pueden añadir múltiples
    # entidades participantes
    entidad_participante = models.CharField(u'Entidad participantes',
                                            max_length=500,
                                            blank=True, null=True)

    aportacion_del_solicitante = models.TextField(
        u'Aportación del solicitante',
        max_length=2048, blank=True, null=True
    )

    created_at = models.DateTimeField(u'Creado', auto_now_add=True)
    updated_at = models.DateTimeField(u'Actualizado', auto_now=True)

    def getFechaFin(self):
        fecha = None
        if self.fecha_de_fin is not None:
            fecha = self.fecha_de_fin
        elif (self.fecha_de_inicio is not None and
              self.duracion_anyos is not None or
              self.duracion_meses is not None or
              self.duracion_dias is not None):
            years = noneToZero(self.duracion_anyos)
            months = noneToZero(self.duracion_meses)
            days = noneToZero(self.duracion_dias)
            delta = datetime.timedelta(days=(days + months * 30 + years * 365))
            fecha = self.fecha_de_inicio + delta
        return fecha

    def __unicode__(self):
        return u'%s' % (self.denominacion_del_proyecto)

    class Meta:
        verbose_name_plural = u'Proyectos'
        ordering = ['-fecha_de_inicio', 'denominacion_del_proyecto']


class Convenio(models.Model):
    """
    https://cvn.fecyt.es/editor/cvn.html?locale\
    =spa#EXPERIENCIA_CIENTIFICA_dataGridProyIDINoComp
    """
    objects = ConvenioManager()
    user_profile = models.ManyToManyField(UserProfile, blank=True, null=True)

    # Campos recomendados
    denominacion_del_proyecto = models.CharField(u'Denominación del proyecto',
                                                 max_length=1000,
                                                 blank=True, null=True)
    numero_de_investigadores = models.IntegerField(
        u'Número de investigadores/as',
        blank=True, null=True
    )

    ### Investigadores responsables
    autores = models.TextField(u'Autores', blank=True, null=True)

    # FIXME: Se permiten multiples instancias
    ### Entidades financiadoras ###
    entidad_financiadora = models.CharField(u'Entidad financiadora',
                                            max_length=500,
                                            blank=True, null=True)
    tipo_de_entidad = models.CharField(u'Tipo de entidad',
                                       max_length=150,
                                       blank=True, null=True)

    ciudad_de_la_entidad = models.CharField(u'Ciudad del trabajo',
                                            max_length=500,
                                            blank=True, null=True)
    pais_de_la_entidad = models.CharField(u'País del trabajo',
                                          max_length=500,
                                          blank=True, null=True)
    comunidad_or_region_entidad = models.CharField(
        u'Autónoma/Reg. del trabajo',
        max_length=500, blank=True, null=True
    )

    calidad_participacion = models.CharField(u'Calidad en que ha participado',
                                             max_length=500,
                                             blank=True, null=True)

    ### Entidades participantes ###
    entidad_participante = models.CharField(u'Entidad participantes',
                                            max_length=500,
                                            blank=True, null=True)

    fecha_de_inicio = models.DateField(u'Fecha de inicio',
                                       blank=True, null=True)
    duracion_anyos = models.IntegerField(u'Duración en años',
                                         blank=True, null=True)
    duracion_meses = models.IntegerField(u'Duración en meses',
                                         blank=True, null=True)
    duracion_dias = models.IntegerField(u'Duración en días',
                                        blank=True, null=True)
    cuantia_total = models.DecimalField(u'Cuantía',
                                        max_digits=19, decimal_places=2,
                                        blank=True, null=True)

    # Más campos
    palabras_clave = models.CharField(u'Describir con palabras clave',
                                      max_length=250,
                                      blank=True, null=True)

    modalidad_del_proyecto = models.CharField(u'Modalidad del proyecto',
                                              max_length=500,
                                              blank=True, null=True)

    ambito = models.CharField(u'Ámbito del convenio',
                              max_length=50, blank=True, null=True)
    otro_ambito = models.CharField(u'Otro ámbito',
                                   max_length=250, blank=True, null=True)

    entidad_de_realizacion = models.CharField(u'Entidad de realización',
                                              max_length=500,
                                              blank=True, null=True)

    ciudad_del_proyecto = models.CharField(u'Ciudad del trabajo',
                                           max_length=250,
                                           blank=True, null=True)
    pais_del_proyecto = models.CharField(u'País del trabajo',
                                         max_length=250,
                                         blank=True, null=True)
    comunidad_or_region_proyecto = models.CharField(
        u'Autónoma/Reg. del trabajo',
        max_length=250, blank=True, null=True
    )

    numero_personas_anyo = models.IntegerField(u'Número personas/año',
                                               blank=True, null=True)

    tipo_proyecto = models.CharField(u'Tipo de proyecto',
                                     max_length=100, blank=True, null=True)
    nombre_del_programa = models.CharField(u'Nombre del programa',
                                           max_length=400,
                                           blank=True, null=True)

    cod_segun_financiadora = models.CharField(u'Código según financiadora',
                                              max_length=100,
                                              blank=True, null=True)
    cuantia_subproyecto = models.DecimalField(u'Cuantía subproyecto',
                                              max_digits=19, decimal_places=2,
                                              blank=True, null=True)
    porcentaje_en_subvencion = models.DecimalField(u'Porcentaje en subvención',
                                                   max_digits=19,
                                                   decimal_places=2,
                                                   blank=True, null=True)
    porcentaje_en_credito = models.DecimalField(u'Porcentaje en crédito',
                                                max_digits=19,
                                                decimal_places=2,
                                                blank=True, null=True)
    porcentaje_mixto = models.DecimalField(u'Porcentaje mixto',
                                           max_digits=19, decimal_places=2,
                                           blank=True, null=True)

    resultados_mas_relevantes = models.CharField(u'Resultados más relevantes',
                                                 max_length=1024,
                                                 blank=True, null=True)
    palabras_clave = models.CharField(u'Describir con palabras clave',
                                      max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(u'Creado', auto_now_add=True)
    updated_at = models.DateTimeField(u'Actualizado', auto_now=True)

    def getFechaFin(self):
        fecha = None
        if (self.fecha_de_inicio is not None and
           self.duracion_anyos is not None or
           self.duracion_meses is not None or
           self.duracion_dias is not None):
            years = noneToZero(self.duracion_anyos)
            months = noneToZero(self.duracion_meses)
            days = noneToZero(self.duracion_dias)
            delta = datetime.timedelta(days=(days + months * 30 + years * 365))
            fecha = self.fecha_de_inicio + delta
        return fecha

    def __unicode__(self):
        return u'%s' % (self.denominacion_del_proyecto)

    class Meta:
        verbose_name_plural = u'Convenios'
        ordering = ['-fecha_de_inicio', 'denominacion_del_proyecto']


############################ Actividad Docente ##########################
class TesisDoctoral(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#EXPERIENCIA_DOCENTE
    """
    objects = TesisDoctoralManager()
    # Campos recomendados
    user_profile = models.ManyToManyField(UserProfile, blank=True, null=True)

    titulo = models.TextField(u'Título del trabajo', blank=True, null=True)
    fecha_de_lectura = models.DateField(u'Fecha de lectura',
                                        blank=True, null=True)

    # Doctorando-a/alumno-a
    autor = models.CharField(u'Autor', max_length=256, blank=True, null=True)

    universidad_que_titula = models.CharField(u'Universidad que titula',
                                              max_length=500,
                                              blank=True, null=True)

    # Más campos
    ciudad_del_trabajo = models.CharField(u'Ciudad del trabajo',
                                          max_length=500,
                                          blank=True, null=True)
    pais_del_trabajo = models.CharField(u'País del trabajo',
                                        max_length=500, blank=True, null=True)
    comunidad_or_region_trabajo = models.CharField(
        u'Comunidad/Región del trabajo',
        max_length=500, blank=True, null=True
    )

    tipo_de_proyecto = models.CharField(u'Tipo de proyecto',
                                        max_length=150, blank=True, null=True)

    codirector = models.CharField(u'Codirector',
                                  max_length=256, blank=True, null=True)

    calificacion = models.CharField(u'Calificación',
                                    max_length=100, blank=True, null=True)

    mencion_de_calidad = models.CharField(u'Mención de calidad',
                                          max_length=4, blank=True, null=True)
    fecha_mencion_de_calidad = models.DateField(u'Fecha mención de calidad',
                                                blank=True, null=True)

    doctorado_europeo = models.CharField(u'Doctorado europeo',
                                         max_length=4, blank=True, null=True)
    fecha_mencion_doctorado_europeo = models.DateField(
        u'Fecha de mención de doctorado europeo',
        blank=True, null=True
    )

    palabras_clave_titulo = models.CharField(u'Palabras clave del título',
                                             max_length=500,
                                             blank=True, null=True)

    created_at = models.DateTimeField(u'Creado', auto_now_add=True)
    updated_at = models.DateTimeField(u'Actualizado', auto_now=True)

    class Meta:
        verbose_name_plural = u'Tesis Doctorales'
        ordering = ['-fecha_de_lectura', 'titulo']
