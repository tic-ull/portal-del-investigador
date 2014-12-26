# -*- encoding: UTF-8 -*-

from .helpers import get_cvn_path, get_old_cvn_path
from core.models import UserProfile
from cvn import settings as st_cvn
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.translation import ugettext_lazy as _
from lxml import etree
from mailing import settings as st_mail
from mailing.send_mail import send_mail
from managers import CongresoManager, ScientificExpManager, CvnItemManager
from parsers.read_helpers import parse_date, parse_nif, parse_cvnitem_to_class
from parsers.write import CvnXmlWriter
from django.conf import settings as st
from core.ws_utils import CachedWS as ws
from helpers import DateRange

import datetime
import fecyt
import logging

logger = logging.getLogger('cvn')


class CVN(models.Model):

    cvn_file = models.FileField(_(u'PDF'), upload_to=get_cvn_path)

    xml_file = models.FileField(_(u'XML'), upload_to=get_cvn_path)

    fecha = models.DateField(_(u'Fecha del CVN'))

    created_at = models.DateTimeField(_(u'Creado'), auto_now_add=True)

    updated_at = models.DateTimeField(_(u'Actualizado'), auto_now=True)

    uploaded_at = models.DateTimeField(
        _(u'PDF Subido'), default=datetime.datetime(2014, 10, 18))

    user_profile = models.OneToOneField(UserProfile)

    status = models.IntegerField(_(u'Estado'), choices=st_cvn.CVN_STATUS)

    is_inserted = models.BooleanField(_(u'Insertado'), default=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        pdf_path = kwargs.pop('pdf_path', None)
        pdf = kwargs.pop('pdf', None)
        super(CVN, self).__init__(*args, **kwargs)
        if user:
            self.user_profile = user.profile
        if pdf_path:
            pdf_file = open(pdf_path)
            pdf = pdf_file.read()
        if pdf and user:
            self.update_from_pdf(pdf, commit=False)

    def update_from_pdf(self, pdf, commit=True):
        CVN.remove_cvn_by_userprofile(self.user_profile)
        self.cvn_file = SimpleUploadedFile(
            'CVN-' + self.user_profile.documento, pdf,
            content_type=st_cvn.PDF)
        (xml, error) = fecyt.pdf2xml(self.cvn_file)
        self.update_fields(xml, commit)

    def update_from_xml(self, xml, commit=True):
        pdf = fecyt.xml2pdf(xml)
        if pdf:
            self.update_from_pdf(pdf, commit)

    def update_fields(self, xml, commit=True):
        self.cvn_file.name = u'CVN-%s.pdf' % self.user_profile.documento
        self.xml_file.save(self.cvn_file.name.replace('pdf', 'xml'),
                           ContentFile(xml), save=False)
        tree_xml = etree.XML(xml)
        self.fecha = parse_date(tree_xml.find('Version/VersionID/Date'))
        self.is_inserted = False
        self.uploaded_at = datetime.datetime.now()
        self.update_status(commit)
        self.xml_file.close()
        if commit:
            self.save()

    def update_status(self, commit=True):
        status = self.status
        if self.fecha <= st_cvn.FECHA_CADUCIDAD:
            self.status = st_cvn.CVNStatus.EXPIRED
        elif not self._is_valid_identity():
            self.status = st_cvn.CVNStatus.INVALID_IDENTITY
        else:
            self.status = st_cvn.CVNStatus.UPDATED
        if self.status != status and commit:
            self.save()

    def _is_valid_identity(self):
        try:
            if self.xml_file.closed:
                self.xml_file.open()
        except IOError:
            return False
        xml_tree = etree.parse(self.xml_file)
        self.xml_file.seek(0)
        nif = parse_nif(xml_tree)
        self.xml_file.close()
        for character in [' ', '-']:
            if character in nif:
                nif = nif.replace(character, '')
        if nif.upper() == self.user_profile.documento.upper():
            return True
        # NIF/NIE without final letter
        if len(nif) == 8 and nif == self.user_profile.documento[:-1]:
            return True
        return False

    @classmethod
    def get_pdf_ull(cls, user, start_date=None, end_date=None):
        parser = CvnXmlWriter(user=user)
        cls._insert_learning_ull(user, parser, start_date, end_date)
        cls._insert_cargos_ull(user, parser, start_date, end_date)
        xml = parser.tostring()
        return fecyt.xml2pdf(xml)

    @staticmethod
    def _insert_learning_ull(user, parser, start_date, end_date):
        items = ws.get(url=st.WS_ULL_LEARNING % user.profile.rrhh_code,
                       use_redis=False)
        for item in items:
            item_date = datetime.datetime.strptime(item["f_expedicion"],
                                                   "%d-%m-%Y").date()
            item_date_range = DateRange(item_date, item_date)
            if not item_date_range.intersect(DateRange(start_date, end_date)):
                continue
            doctor = item["des1_grado_titulacion"] == u'Doctor'
            university = item.pop("organismo", None)
            if doctor:
                parser.add_learning_phd(title=item["des1_titulacion"],
                                        date=item_date,
                                        university=university)
            else:
                parser.add_learning(title=item["des1_titulacion"],
                                    title_type=item["des1_grado_titulacion"],
                                    university=university,
                                    date=item_date)

    @staticmethod
    def _insert_cargos_ull(user, parser, start_date, end_date):
        items = ws.get(url=st.WS_ULL_CARGOS % user.profile.rrhh_code,
                       use_redis=False)
        for item in items:
            item["start_date"] = datetime.datetime.strptime(
                item.pop("f_toma_posesion"), "%d-%m-%Y").date()
            if "f_hasta" in item:
                item["end_date"] = datetime.datetime.strptime(
                    item.pop("f_hasta"), "%d-%m-%Y").date()
            else:
                item["end_date"] = None
            item_date_range = DateRange(item["start_date"], item["end_date"])
            if not item_date_range.intersect(DateRange(start_date, end_date)):
                continue
            item["title"] = item.pop("des1_cargo")
            item["centre"] = item.pop("centro", None)
            item["department"] = item.pop("departamento", None)
            item["full_time"] = item.pop("dedicacion",
                                         None) == "Tiempo Completo"
            parser.add_profession(**item)

    @classmethod
    def remove_cvn_by_userprofile(cls, user_profile):
        try:
            cvn_old = cls.objects.get(user_profile=user_profile)
            cvn_old.remove()
        except ObjectDoesNotExist:
            pass

    @staticmethod
    def create(user, xml=None):
        if not xml:
            parser = CvnXmlWriter(user=user)
            xml = parser.tostring()
        pdf = fecyt.xml2pdf(xml)
        if pdf is None:
            return None
        cvn = CVN(user=user, pdf=pdf)
        cvn.save()
        return cvn

    def remove(self):
        # Removes data related to CVN that is not on the CVN class.
        self._backup_pdf()
        if self.cvn_file:
            self.cvn_file.delete(False)  # Remove PDF file
        if self.xml_file:
            self.xml_file.delete(False)  # Remove XML file

    def _backup_pdf(self):
        filename = self.cvn_file.name.split('/')[-1].replace(
            u'.pdf', u'-' + str(
                self.uploaded_at.strftime('%Y-%m-%d-%Hh%Mm%Ss')
            ) + u'.pdf')

        old_cvn_file = SimpleUploadedFile(
            filename, self.cvn_file.read(), content_type=st_cvn.PDF)

        cvn_old = OldCvnPdf(
            user_profile=self.user_profile, cvn_file=old_cvn_file,
            uploaded_at=self.uploaded_at)
        cvn_old.save()

    def remove_producciones(self):
        Articulo.remove_by_userprofile(self.user_profile)
        Libro.remove_by_userprofile(self.user_profile)
        Capitulo.remove_by_userprofile(self.user_profile)
        Congreso.remove_by_userprofile(self.user_profile)
        Proyecto.remove_by_userprofile(self.user_profile)
        Convenio.remove_by_userprofile(self.user_profile)
        TesisDoctoral.remove_by_userprofile(self.user_profile)
        Patente.remove_by_userprofile(self.user_profile)

    def insert_xml(self):
        try:
            if self.xml_file.closed:
                self.xml_file.open()
            self.xml_file.seek(0)
            cvn_items = etree.parse(self.xml_file).findall('CvnItem')
            self._parse_cvn_items(cvn_items)
            self.is_inserted = True
            self.save()
        except IOError:
            if self.xml_file:
                logger.error((u'No existe el fichero' + u' %s') % (
                    self.xml_file.name))
            else:
                logger.warning(u'Se requiere de un fichero CVN-XML')

    def _parse_cvn_items(self, cvn_items):
        for cvnitem in cvn_items:
            produccion = parse_cvnitem_to_class(cvnitem)
            if produccion is None:
                continue
            produccion.objects.create(cvnitem, self.user_profile)

    def __unicode__(self):
        return '%s ' % self.cvn_file.name.split('/')[-1]

    class Meta:
        verbose_name_plural = _(u'Currículum Vitae Normalizado')
        ordering = ['-uploaded_at', '-updated_at']


class Publicacion(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#ACTIVIDAD_CIENTIFICA
    """

    objects = CvnItemManager()

    titulo = models.TextField(
        _(u'Título de la publicación'), blank=True, null=True)

    user_profile = models.ManyToManyField(UserProfile, blank=True, null=True)

    fecha = models.DateField(_(u'Fecha'), blank=True, null=True)

    nombre_publicacion = models.TextField(
        _(u'Nombre de la publicación'), blank=True, null=True)

    volumen = models.CharField(
        _(u'Volumen'), max_length=100, blank=True, null=True)

    numero = models.CharField(
        _(u'Número'), max_length=100, blank=True, null=True)

    pagina_inicial = models.CharField(
        _(u'Página Inicial'), max_length=100, blank=True, null=True)

    pagina_final = models.CharField(
        _(u'Página Final'), max_length=100, blank=True, null=True)

    autores = models.TextField(_(u'Autores'), blank=True, null=True)

    isbn = models.CharField(_(u'ISBN'), max_length=150, blank=True, null=True)

    issn = models.CharField(_(u'ISSN'), max_length=150, blank=True, null=True)

    deposito_legal = models.CharField(
        _(u'Depósito legal'), max_length=150, blank=True, null=True)

    created_at = models.DateTimeField(_(u'Creado'), auto_now_add=True)

    updated_at = models.DateTimeField(_(u'Actualizado'), auto_now=True)

    # tipo_de_soporte = models.CharField(_(u'Tipo de soporte'),
    #                                    max_length=1000, blank=True,
    #                                    null=True)
    # Publicaciones con nombre de hasta 1400 caracteres
    # editorial = models.CharField(_(u'Editorial'),
    #                              max_length=500, blank=True, null=True)
    # Otros campos
    # posicion_sobre_total = models.IntegerField(_(u'Posición sobre total'),
    #                                            blank=True, null=True)
    # en_calidad_de = models.CharField(_(u'En calidad de'),
    #                                  max_length=500, blank=True, null=True)
    # url = models.URLField(_(u'URL'), max_length=500, blank=True, null=True)
    # coleccion = models.CharField(_(u'Colección'),
    #                              max_length=150, blank=True, null=True)
    # ciudad = models.CharField(_(u'Ciudad'),
    #                           max_length=500,  blank=True, null=True)
    # pais = models.CharField(_(u'País'),
    #                         max_length=500, blank=True, null=True)
    # comunidad_or_region = models.CharField(_(u'Autónoma/Reg. de trabajo'),
    #                                        max_length=500,
    #                                        blank=True, null=True)
    # Índice de impacto
    # fuente_de_impacto = models.CharField(_(u'Fuente de impacto'),
    #                                    max_length=500, blank=True, null=True)
    # categoria = models.CharField(_(u'Categoría'),
    #                              max_length=500, blank=True, null=True)
    # indice_de_impacto = models.CharField(_(u'Índice de impacto'),
    #                                    max_length=500, blank=True, null=True)
    # posicion = models.IntegerField(_(u'Posicion'), blank=True, null=True)
    # num_revistas = models.IntegerField(
    #     _(u'Número de revistas en la categoría'),
    #     blank=True, null=True)
    # revista_25 = models.CharField(_(u'Revista dentro del 25%'),
    #                               max_length=50, blank=True, null=True)
    # Citas
    # fuente_de_citas = models.CharField(_(u'Fuente de citas'),
    #                                    max_length=500, blank=True, null=True)
    # citas = models.CharField(_(u'Citas'), max_length=500,
    #                          blank=True, null=True)
    # publicacion_relevante = models.CharField(_(u'Publicación relevante'),
    #                                          max_length=50,
    #                                          blank=True, null=True)
    # resenyas_en_revista = models.CharField(_(u'Reseñas en revistas'),
    #                                        max_length=500,
    #                                        blank=True, null=True)
    # filtro = models.CharField(_(u'Filtro'), max_length=500,
    #                           blank=True, null=True)
    # resultados_destacados = models.TextField(_(u'Resultados destacados'),
    #                                          blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.titulo

    class Meta:
        verbose_name_plural = _(u'Publicaciones')
        ordering = ['-fecha', 'titulo']
        abstract = True


class Articulo(Publicacion):

    @classmethod
    def remove_by_userprofile(cls, user_profile):
        user_profile.articulo_set.remove(
            *user_profile.articulo_set.all())
        cls.objects.filter(user_profile__isnull=True).delete()

    class Meta:
        verbose_name_plural = _(u'Artículos')
        ordering = ['-fecha', 'titulo']


class Libro(Publicacion):

    @classmethod
    def remove_by_userprofile(cls, user_profile):
        user_profile.libro_set.remove(
            *user_profile.libro_set.all())
        cls.objects.filter(user_profile__isnull=True).delete()

    class Meta:
        verbose_name_plural = _(u'Libros')
        ordering = ['-fecha', 'titulo']


class Capitulo(Publicacion):

    @classmethod
    def remove_by_userprofile(cls, user_profile):
        user_profile.capitulo_set.remove(
            *user_profile.capitulo_set.all())
        cls.objects.filter(user_profile__isnull=True).delete()

    class Meta:
        verbose_name_plural = _(u'Capítulos de Libros')
        ordering = ['-fecha', 'titulo']


class Congreso(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#ACTIVIDAD_CIENTIFICA
    """

    objects = CongresoManager()

    user_profile = models.ManyToManyField(UserProfile, blank=True, null=True)

    titulo = models.TextField(_(u'Título'), blank=True, null=True)

    fecha_de_inicio = models.DateField(
        _(u'Fecha de realización'), blank=True, null=True)

    fecha_de_fin = models.DateField(
        _(u'Fecha de finalización'), blank=True, null=True)

    nombre_del_congreso = models.TextField(
        _(u'Nombre del congreso'), blank=True, null=True)

    ciudad_de_realizacion = models.CharField(
        _(u'Ciudad de realización'), max_length=500, blank=True, null=True)

    autores = models.TextField(_(u'Autores'), blank=True, null=True)

    fecha = models.DateField(_(u'Fecha'), blank=True, null=True)

    ambito = models.CharField(
        _(u'Ámbito del congreso'), max_length=50, blank=True, null=True)

    otro_ambito = models.CharField(
        _(u'Otro ámbito'), max_length=250, blank=True, null=True)

    deposito_legal = models.CharField(
        _(u'Depósito legal'), max_length=150, blank=True, null=True)

    publicacion_acta_congreso = models.CharField(
        _(u'Publicación en acta'), max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(_(u'Creado'), auto_now_add=True)

    updated_at = models.DateTimeField(_(u'Actualizado'), auto_now=True)

    # pais_de_realizacion = models.CharField(_(u'País de realización'),
    #                                        max_length=500,
    #                                        blank=True, null=True)
    # comunidad_or_region_realizacion = models.CharField(
    #     _(u'Comunidad/Región de realizacion'),
    #     max_length=500, blank=True, null=True
    # )
    # entidad_organizadora = models.CharField(_(u'Entidad organizadora'),
    #                                         max_length=250,
    #                                         blank=True, null=True)
    # ciudad = models.CharField(_(u'Ciudad'), max_length=500,
    #                           blank=True, null=True)
    # pais = models.CharField(_(u'País'), max_length=500, blank=True,
    #                         null=True)
    # comunidad_or_region = models.CharField(_(u'Comunidad autónoma/Región'),
    #                                        max_length=500,
    #                                        blank=True, null=True)
    # titulo_publicacion = models.CharField(_(u'Título de la publicación'),
    #                                       max_length=250,
    #                                       blank=True, null=True)
    # tipo_evento = models.CharField(_(u'Tipo evento'),
    #                                max_length=50, blank=True, null=True)
    # tipo = models.CharField(_(u'Tipo'), max_length=250, blank=True,
    #                         null=True)
    # nombre_de_publicacion = models.CharField(_(u'Nombre de la publicación'),
    #                                          max_length=250,
    #                                          blank=True, null=True)
    # comite_admision_externa = models.CharField(
    #     _(u'Con comité de admisión externa'),
    #     max_length=250, blank=True, null=True
    # )
    # tipo_de_participacion = models.CharField(_(u'Tipo de participación'),
    #                                          max_length=250,
    #                                          blank=True, null=True)
    # intervencion_por = models.CharField(_(u'Intevención por'),
    #                                     max_length=250,
    #                                     blank=True, null=True)
    # volumen = models.CharField(_(u'Volumen'),
    #                            max_length=100, blank=True, null=True)
    # numero = models.CharField(_(u'Número'), max_length=100,
    #                           blank=True, null=True)
    # pagina_inicial = models.CharField(_(u'Página Inicial'),
    #                                   max_length=100, blank=True, null=True)
    # pagina_final = models.CharField(_(u'Página Final'),
    #                                 max_length=100, blank=True, null=True)
    # editorial = models.CharField(_(u'Editorial'),
    #                              max_length=500, blank=True, null=True)
    # isbn = models.CharField(_(u'ISBN'), max_length=150,
    #                         blank=True, null=True)
    # issn = models.CharField(_(u'ISSN'), max_length=150,
    #                         blank=True, null=True)
    # url = models.URLField(_(u'URL'), max_length=500, blank=True, null=True)
    # pais = models.CharField(_(u'País'), max_length=500,
    #                         blank=True, null=True)
    # comunidad_or_region = models.CharField(_(u'Comunidad Autónoma/Región'),
    #                                        max_length=500,
    #                                        blank=True, null=True)

    @classmethod
    def remove_by_userprofile(cls, user_profile):
        user_profile.congreso_set.remove(
            *user_profile.congreso_set.all())
        cls.objects.filter(user_profile__isnull=True).delete()

    def __unicode__(self):
        return "%s" % self.titulo

    class Meta:
        verbose_name_plural = _(u'Congresos')
        ordering = ['-fecha_de_inicio', 'titulo']


class ScientificExp(models.Model):

    objects = ScientificExpManager()

    user_profile = models.ManyToManyField(UserProfile, blank=True, null=True)

    titulo = models.CharField(
        _(u'Denominación'), max_length=1000, blank=True, null=True)

    numero_de_investigadores = models.IntegerField(
        _(u'Número de investigadores/as'), blank=True, null=True)

    autores = models.TextField(_(u'Autores'), blank=True, null=True)

    fecha_de_inicio = models.DateField(
        _(u'Fecha de inicio'), blank=True, null=True)

    fecha_de_fin = models.DateField(
        _(u'Fecha de finalización'), blank=True, null=True)

    duracion = models.IntegerField(
        _(u'Duración (en días)'), blank=True, null=True)

    ambito = models.CharField(
        _(u'Ámbito'), max_length=50, blank=True, null=True)

    otro_ambito = models.CharField(
        _(u'Otro ámbito'), max_length=250, blank=True, null=True)

    cod_segun_financiadora = models.CharField(
        _(u'Código según financiadora'), max_length=150, blank=True, null=True)

    cuantia_total = models.CharField(
        _(u'Cuantía'), max_length=19, blank=True, null=True)

    cuantia_subproyecto = models.CharField(
        _(u'Cuantía subproyecto'), max_length=19, blank=True, null=True)

    porcentaje_en_subvencion = models.CharField(
        _(u'Porcentaje en subvención'), max_length=19, blank=True, null=True)

    porcentaje_en_credito = models.CharField(
        _(u'Porcentaje en crédito'), max_length=19, blank=True, null=True)

    porcentaje_mixto = models.CharField(
        _(u'Porcentaje mixto'), max_length=19, blank=True, null=True)

    created_at = models.DateTimeField(_(u'Creado'), auto_now_add=True)

    updated_at = models.DateTimeField(_(u'Actualizado'), auto_now=True)

    def __unicode__(self):
        return u'%s' % self.titulo

    def save(self, *args, **kwargs):

        # If we update fecha_de_fin or duracion we must calculate the other
        # field. To check which one was modified we compare with old version.
        try:
            old = type(self).objects.get(pk=self.pk)
        except ObjectDoesNotExist:
            pass
        else:
            inicio_changed = (old.fecha_de_inicio != self.fecha_de_inicio
                              and self.fecha_de_inicio is not None)
            fin_changed = (old.fecha_de_fin != self.fecha_de_fin
                           and self.fecha_de_fin is not None)
            duracion_changed = (old.duracion != self.duracion and
                                self.duracion is not None)
            if inicio_changed or fin_changed:
                duracion = self.fecha_de_fin - self.fecha_de_inicio
                self.duracion = duracion.days
            elif duracion_changed:
                self.fecha_de_fin = (self.fecha_de_inicio +
                                     datetime.timedelta(days=self.duracion))
        # We do the save afterwards
        super(ScientificExp, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _(u'Experiencia Científica')
        ordering = ['-fecha_de_inicio', 'titulo']
        abstract = True


class Convenio(ScientificExp):
    """
    https://cvn.fecyt.es/editor/cvn.html?locale\
    =spa#EXPERIENCIA_CIENTIFICA_dataGridProyIDINoComp
    """

    @classmethod
    def remove_by_userprofile(cls, user_profile):
        user_profile.convenio_set.remove(
            *user_profile.convenio_set.all())
        cls.objects.filter(user_profile__isnull=True).delete()

    class Meta(ScientificExp.Meta):
        verbose_name_plural = _(u'Convenios')
        ordering = ['-fecha_de_inicio', 'titulo']


class Proyecto(ScientificExp):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale\
        =spa#EXPERIENCIA_CIENTIFICA_dataGridProyIDIComp
    """

    @classmethod
    def remove_by_userprofile(cls, user_profile):
        user_profile.proyecto_set.remove(
            *user_profile.proyecto_set.all())
        cls.objects.filter(user_profile__isnull=True).delete()

    class Meta:
        verbose_name_plural = _(u'Proyectos')
        ordering = ['-fecha_de_inicio', 'titulo']


class TesisDoctoral(models.Model):
    """
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#EXPERIENCIA_DOCENTE
    """

    objects = CvnItemManager()

    user_profile = models.ManyToManyField(UserProfile, blank=True, null=True)

    titulo = models.TextField(_(u'Título del trabajo'), blank=True, null=True)

    fecha = models.DateField(_(u'Fecha de lectura'), blank=True, null=True)

    autor = models.CharField(
        _(u'Autor'), max_length=256, blank=True, null=True)

    universidad_que_titula = models.CharField(_(
        u'Universidad que titula'), max_length=500, blank=True, null=True)

    codirector = models.CharField(
        _(u'Codirector'), max_length=256, blank=True, null=True)

    created_at = models.DateTimeField(_(u'Creado'), auto_now_add=True)

    updated_at = models.DateTimeField(_(u'Actualizado'), auto_now=True)

    # ciudad_del_trabajo = models.CharField(_(u'Ciudad del trabajo'),
    #                                       max_length=500,
    #                                       blank=True, null=True)
    # pais_del_trabajo = models.CharField(_(u'País del trabajo'),
    #                                     max_length=500, blank=True,
    #                                     null=True)
    # comunidad_or_region_trabajo = models.CharField(
    #     _(u'Comunidad/Región del trabajo'),
    #     max_length=500, blank=True, null=True
    # )
    # tipo_de_proyecto = models.CharField(_(u'Tipo de proyecto'),
    #                                     max_length=150, blank=True,
    #                                     null=True)
    # calificacion = models.CharField(_(u'Calificación'),
    #                                 max_length=100, blank=True, null=True)
    # mencion_de_calidad = models.CharField(_(u'Mención de calidad'),
    #                                       max_length=4, blank=True,
    #                                       null=True)
    # fecha_mencion_de_calidad = models.DateField(
    #     _(u'Fecha mención de calidad'), blank=True, null=True)
    # doctorado_europeo = models.CharField(_(u'Doctorado europeo'),
    #                                      max_length=4, blank=True, null=True)
    # fecha_mencion_doctorado_europeo = models.DateField(
    #     _(u'Fecha de mención de doctorado europeo'),
    #     blank=True, null=True
    # )
    # palabras_clave_titulo = models.CharField(_(u'Palabras clave del título'),
    #                                          max_length=500,
    #                                          blank=True, null=True)

    @classmethod
    def remove_by_userprofile(cls, user_profile):
        user_profile.tesisdoctoral_set.remove(
            *user_profile.tesisdoctoral_set.all())
        cls.objects.filter(user_profile__isnull=True).delete()

    def __unicode__(self):
        return "%s" % self.titulo

    class Meta:
        verbose_name_plural = _(u'Tesis Doctorales')
        ordering = ['-fecha', 'titulo']


class Patente(models.Model):
    """
    https://cvn.fecyt.es/editor/cvn.html?locale=spa#EXPERIENCIA_CIENTIFICA
    """

    objects = CvnItemManager()

    user_profile = models.ManyToManyField(UserProfile, blank=True, null=True)

    titulo = models.TextField(_(u'Denominación'), blank=True, null=True)

    fecha = models.DateField(_(u'Fecha'), blank=True, null=True)

    fecha_concesion = models.DateField(
        _(u'Fecha de concesión'), blank=True, null=True)

    num_solicitud = models.CharField(
        _(u'Número de solicitud'), max_length=100, blank=True, null=True)

    lugar_prioritario = models.CharField(
        _(u'País de prioridad'), max_length=100, blank=True, null=True)

    lugares = models.TextField(_(u'Países'), blank=True, null=True)

    autores = models.TextField(_(u'Autores'), blank=True, null=True)

    entidad_titular = models.CharField(
        _(u'Entidad titular'), max_length=255, blank=True, null=True)

    empresas = models.TextField(_(u'Empresas'), blank=True, null=True)

    created_at = models.DateTimeField(_(u'Creado'), auto_now_add=True)

    updated_at = models.DateTimeField(_(u'Actualizado'), auto_now=True)

    @classmethod
    def remove_by_userprofile(cls, user_profile):
        user_profile.patente_set.remove(
            *user_profile.patente_set.all())
        cls.objects.filter(user_profile__isnull=True).delete()

    def __unicode__(self):
        return "%s" % self.titulo

    class Meta:
        verbose_name_plural = _(u'Propiedades Intelectuales')
        ordering = ['-fecha', 'titulo']


class OldCvnPdf(models.Model):

    user_profile = models.ForeignKey(UserProfile)

    cvn_file = models.FileField(_(u'PDF'), upload_to=get_old_cvn_path)

    uploaded_at = models.DateTimeField(_(u'PDF Subido'))

    created_at = models.DateTimeField(_(u'Creado'), auto_now_add=True)

    updated_at = models.DateTimeField(_(u'Actualizado'), auto_now=True)

    def __unicode__(self):
        return '%s ' % self.cvn_file.name.split('/')[-1]

    class Meta:
        verbose_name_plural = _(u'Histórico de Currículum Vitae Normalizado')
        ordering = ['-uploaded_at']
