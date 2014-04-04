# -*- encoding: UTF-8 -*-

from cvn.utils import noneToZero
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from cvn.settings import XML_ROOT, PDF_ROOT
import datetime


class PublicacionManager(models.Manager):

    def byUsuariosYearTipo(self, usuarios, year, tipo):
        return super(PublicacionManager, self).get_query_set().filter(
            Q(usuario__in=usuarios) &
            Q(fecha__year=year) &
            Q(tipo_de_produccion=tipo)
        ).distinct().order_by('fecha')


class CongresoManager(models.Manager):

    def byUsuariosYear(self, usuarios, year):
        return super(CongresoManager, self).get_query_set().filter(
            Q(usuario__in=usuarios) &
            Q(fecha_realizacion__year=year)
        ).distinct().order_by('fecha_realizacion')


class TesisDoctoralManager(models.Manager):

    def byUsuariosYear(self, usuarios, year):
        return super(TesisDoctoralManager, self).get_query_set().filter(
            Q(usuario__in=usuarios) &
            Q(fecha_de_lectura__year=year)
        ).distinct().order_by('fecha_de_lectura')


class ProyectoConvenioManager(models.Manager):

    def byUsuariosYear(self, usuarios, year):
        fechaInicioMax = datetime.date(year, 12, 31)
        fechaFinMin = datetime.date(year, 1, 1)
        elements = super(ProyectoConvenioManager, self).get_query_set().filter(
            Q(usuario__in=usuarios) &
            Q(fecha_de_inicio__isnull=False) &
            Q(fecha_de_inicio__lte=fechaInicioMax)
        ).distinct().order_by('fecha_de_inicio')
        elements_list = []
        for element in elements:
            fechaFin = element.getFechaFin()
            if fechaFin is None:
                fechaFin = element.fecha_de_inicio
            if fechaFin >= fechaFinMin:
                elements_list.append(element)
        return elements_list


###### Curriculum Vitae Normalizado (Aplicación Viinv) ######
class CVN(models.Model):
    """
     Esta tabla almacena los datos referentes al CVN del usuario.
     Ha sido importada de la aplicación antigua del portal del
     investigador.
    """
    cvn_file = models.FileField(upload_to=PDF_ROOT)
    xml_file = models.FileField(upload_to=XML_ROOT)
    fecha_cvn = models.DateField()
    created_at = models.DateTimeField(u'Creado', auto_now_add=True)
    updated_at = models.DateTimeField(u'Actualizado', auto_now=True)

    def __unicode__(self):
        return u'%s con fecha %s' % (self.cvn_file, self.fecha_cvn,)


# Modelo para almacenar los datos del investigador del FECYT
class Usuario(models.Model):
    """
        Datos personales del usuario
        https://cvn.fecyt.es/editor/cvn.html?locale=spa#IDENTIFICACION
    """
    user = models.OneToOneField(User)
    cvn = models.OneToOneField(CVN, on_delete=models.SET_NULL,
                               null=True, blank=True)
    documento = models.CharField(u'Documento', max_length=20,
                                 blank=True, null=True, unique=True)
    rrhh_code = models.CharField(u'Código persona', max_length=20,
                                 blank=True, null=True, unique=True)

    def __unicode__(self):
        return self.user.username


class Publicacion(models.Model):
    """
        Publicaciones, documentos científicos y técnicos.

        https://cvn.fecyt.es/editor/cvn.html?locale=spa#ACTIVIDAD_CIENTIFICA
    """
    objects = PublicacionManager()
    # Campo recomendado
    titulo = models.TextField(u'Título de la publicación',
                              blank=True, null=True)

    # Una publicación puede pertenecer a varios usuarios.
    usuario = models.ManyToManyField(Usuario, blank=True, null=True)

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
        Trabajos presentados en congresos nacionales o internacionales.

        # https://cvn.fecyt.es/editor/cvn.html?locale=spa#ACTIVIDAD_CIENTIFICA
    """
    objects = CongresoManager()
    usuario = models.ManyToManyField(Usuario, blank=True, null=True)

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


################### Experiencia científica y tecnológica ####################
class Proyecto(models.Model):
    """
        Participación en proyectos de I+D+i financiados en convocatorias
        competitivas de Administraciones o entidades públicas y privadas.

        https://cvn.fecyt.es/editor/cvn.html?locale\
        =spa#EXPERIENCIA_CIENTIFICA_dataGridProyIDIComp
    """
    objects = ProyectoConvenioManager()
    usuario = models.ManyToManyField(Usuario, blank=True, null=True)

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


class Convenio(models.Model):
    """
    Participación en contratos, convenios o proyectos de I+D+i
    no competitivos con Administraciones o entidades públicas o privadas

    https://cvn.fecyt.es/editor/cvn.html?locale\
    =spa#EXPERIENCIA_CIENTIFICA_dataGridProyIDINoComp
    """
    objects = ProyectoConvenioManager()
    usuario = models.ManyToManyField(Usuario, blank=True, null=True)

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


############################ Actividad Docente ##########################
class TesisDoctoral(models.Model):
    """
        Dirección de tesis doctorales y/o proyectos fin de carrera

        https://cvn.fecyt.es/editor/cvn.html?locale=spa#EXPERIENCIA_DOCENTE
    """
    objects = TesisDoctoralManager()
    # Campos recomendados
    usuario = models.ManyToManyField(Usuario, blank=True, null=True)

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

    def __unicode__(self):
        return u'%s de fecha %s' % (self.titulo, self.fecha_de_lectura)

    class Meta:
        verbose_name_plural = u'Tesis Doctorales'


########## TABLAS IMPORTADAS VIINV ##########
###### Tabla investigador  ######
'''class Investigador(models.Model):
    """
     Esta tabla alamecena los datos correspondientes al investigador.
     Ha sido importada de la aplicación antigua del portal del
     investigador.
    """
    usuario = models.ForeignKey('Usuario')
    nombre = models.CharField(u'Nombre',
                              max_length=50,
                              blank=True,
                              null=True)
    primer_apellido = models.CharField(u'Primer Apellido',
                                       max_length=50,
                                       blank=True,
                                       null=True)
    segundo_apellido = models.CharField(u'Segundo Apellido',
                                        max_length=50,
                                        blank=True,
                                        null=True)
    nif = models.CharField(u'Documento', max_length=10)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=6)
    email = models.CharField(max_length=60)
    telefono = models.CharField(max_length=60, blank=True)
    dedicacion = models.CharField(max_length=8)
    file = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    confirma_grupo_a = models.IntegerField(null=True, blank=True,
                                           db_column='confirma_grupo_A')
    confirma_grupo_b = models.IntegerField(null=True, blank=True,
                                           db_column='confirma_grupo_B')
    sexenios = models.IntegerField(null=True, blank=True)
    inicio_sexenio = models.DateField(null=True, blank=True)
    fin_sexenio = models.DateField(null=True, blank=True)
    cas_username = models.CharField(max_length=100, blank=True)
    cod_persona = models.CharField(max_length=5)
    cese = models.DateField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_last_update = models.DateTimeField(null=True, blank=True)
#    rrhh_id = models.IntegerField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = u'Investigadores'
'''
