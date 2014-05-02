# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.utils import noneToZero
from django.conf import settings as st
from django.contrib.auth.models import User
from django.core.files.move import file_move_safe
from django.db import models
from lxml import etree
from managers import (PublicacionManager, CongresoManager, ProyectoManager,
                      ConvenioManager, TesisDoctoralManager)
from parser_helpers import (parse_produccion_type, parse_produccion_subtype,
                            parse_nif)
import base64
import datetime
import logging
import os
import suds
import sys
import time


logger = logging.getLogger(__name__)


class FECYT(models.Model):

    @staticmethod
    def get_produccion_from_code(code, subtype):
        if code == '':
            return None
        if code == 'TesisDoctoral' and subtype != 'TesisDoctoral':
            return None
        if code == 'Publicacion':
            code = subtype
        return getattr(sys.modules[__name__], code)

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


class UserProfile(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#IDENTIFICACION
    """
    user = models.OneToOneField(User, related_name='profile')
    documento = models.CharField(u'Documento', max_length=20,
                                 blank=True, null=True, unique=True)
    rrhh_code = models.CharField(u'Código persona', max_length=20,
                                 blank=True, null=True, unique=True)

    def __unicode__(self):
        return self.user.username

    def can_upload_cvn(self, xml):
        xml_tree = etree.XML(xml)
        nif = parse_nif(xml_tree)
        if (self.user.has_perm('can_upload_other_users_cvn') or
           nif.upper() == self.user.profile.documento.upper()):
            return True
        return False


class CVN(models.Model):
    cvn_file = models.FileField(u'PDF', upload_to=stCVN.PDF_ROOT)
    xml_file = models.FileField(u'XML', upload_to=stCVN.XML_ROOT)
    fecha_cvn = models.DateField(u'Fecha del CVN')
    created_at = models.DateTimeField(u'Creado', auto_now_add=True)
    updated_at = models.DateTimeField(u'Actualizado', auto_now=True)
    user_profile = models.OneToOneField(UserProfile)

    class Meta:
        verbose_name_plural = u'Currículum Vitae Normalizado'

    def __unicode__(self):
        return u'%s con fecha %s' % (self.cvn_file, self.fecha_cvn)

    def remove(self):
        # Removes data related to CVN that is not on the CVN class.
        self._backup_pdf()
        if self.xml_file:
            self.xml_file.delete()      # Remove xml file
        self._remove_producciones()     # Removed info related to cvn

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
            code = parse_produccion_type(CVNItem)
            subtype = parse_produccion_subtype(CVNItem)
            produccion = FECYT.get_produccion_from_code(code, subtype)
            if produccion is None:
                continue
            produccion.objects.create(CVNItem, self.user_profile)


class Publicacion(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#ACTIVIDAD_CIENTIFICA
    """
    # FECYT_CODE = stCVN.FECYT_CODE['Publicacion']
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

    objects = PublicacionManager()

    class Meta:
        verbose_name_plural = u'Artículos'


class Libro(Publicacion):

    objects = PublicacionManager()

    class Meta:
        verbose_name_plural = u'Libros'


class Capitulo(Publicacion):

    objects = PublicacionManager()

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


# ################## Experiencia científica y tecnológica ####################
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

    # Investigadores responsables
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

    # Entidades financiadoras
    # FIXME En el editor de la FECYT se pueden añadir múltiples
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

    # Entidades participantes
    # FIXME En el editor de la FECYT se pueden añadir múltiples
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

    # Investigadores responsables
    autores = models.TextField(u'Autores', blank=True, null=True)

    # FIXME: Se permiten multiples instancias
    # Entidades financiadoras ###
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

    # Entidades participantes
    entidad_participante = models.CharField(u'Entidad participantes',
                                            max_length=500,
                                            blank=True, null=True)

    fecha_de_inicio = models.DateField(u'Fecha de inicio',
                                       blank=True, null=True)
    fecha_de_fin = models.DateField(u'Fecha de finalización',
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


# ########################### Actividad Docente ##########################
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
