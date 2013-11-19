# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from __future__ import unicode_literals
from django.db import models
from cvn.settings import XML_ROOT, PDF_ROOT

class AccseConvocatoria(models.Model):
    id = models.IntegerField(primary_key=True)
    num_convocatoria = models.IntegerField()
    fecha_inicio_aplicacion = models.DateField()
    fecha_final_aplicacion = models.DateField()
    fecha_inicio_presentacion = models.DateField()
    fecha_final_presentacion = models.DateField()
    fecha_inicio_validacion = models.DateField()
    fecha_fin_validacion = models.DateField()
    fecha_inicio_autorizacion = models.DateField()
    fecha_final_autorizacion = models.DateField()
    fecha_apertura_convocatoria = models.DateField(null=True, blank=True)
    fecha_cierre_convocatoria = models.DateField(null=True, blank=True)
    notificada = models.IntegerField(null=True, blank=True)
    resolucion_provisional = models.DateTimeField(null=True, blank=True)
    resolucion_definitiva = models.DateTimeField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    plazo_justificacion = models.IntegerField(null=True, blank=True)
    tipo_convocatoria = models.CharField(max_length=30L, blank=True)
    class Meta:
        db_table = 'Accse_convocatoria'

class AccseEstadosolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    confirmada = models.IntegerField()
    rectificada = models.IntegerField()
    cancelada = models.IntegerField()
    valorada = models.IntegerField()
    concedida = models.IntegerField()
    desestimada = models.IntegerField()
    reclamada = models.IntegerField()
    renunciada = models.IntegerField()
    justificada = models.IntegerField(null=True, blank=True)
    archivada = models.IntegerField()
    anio = models.IntegerField()
    plazo = models.CharField(max_length=30L)
    propuesta = models.CharField(max_length=30L, blank=True)
    resolucion = models.CharField(max_length=30L)
    cantidad_concedida = models.FloatField(null=True, blank=True)
    razon_desestimacion = models.TextField(blank=True)
    observaciones_val = models.TextField(blank=True)
    observaciones_aut = models.TextField(blank=True)
    observaciones_int = models.TextField(blank=True)
    historial_comm = models.TextField(blank=True)
    notificado_inicio_justificacion = models.IntegerField()
    momento_creacion = models.DateTimeField(null=True, blank=True)
    fecha_registro_entrada = models.DateField(null=True, blank=True)
    momento_registro_entrada = models.DateTimeField(null=True, blank=True)
    fecha_limite_rectificacion = models.DateField(null=True, blank=True)
    momento_rectificacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_aceptacion = models.DateField(null=True, blank=True)
    fecha_carta_aceptacion = models.DateField(null=True, blank=True)
    momento_carta_aceptacion = models.DateTimeField(null=True, blank=True)
    momento_renuncia = models.DateTimeField(null=True, blank=True)
    momento_cancelacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_reclamacion = models.DateField(null=True, blank=True)
    momento_reclamacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_justificacion = models.DateField(null=True, blank=True)
    momento_justificacion = models.DateTimeField(null=True, blank=True)
    fichero_registro_entrada = models.CharField(max_length=100L, blank=True)
    fichero_carta_aceptacion = models.CharField(max_length=100L, blank=True)
    solicitud = models.ForeignKey('AccseSolicitud')
    class Meta:
        db_table = 'Accse_estadosolicitud'

class AccseFilejustificacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AccseSolicitud')
    class Meta:
        db_table = 'Accse_filejustificacion'

class AccseFilereclamacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AccseSolicitud')
    class Meta:
        db_table = 'Accse_filereclamacion'

class AccseFilesubsanacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AccseSolicitud')
    class Meta:
        db_table = 'Accse_filesubsanacion'

class AccseInvitado(models.Model):
    id = models.IntegerField(primary_key=True)
    solicitud = models.ForeignKey('AccseSolicitud')
    primer_apellido = models.CharField(max_length=30L)
    segundo_apellido = models.CharField(max_length=30L, blank=True)
    nombre = models.CharField(max_length=30L)
    centro = models.CharField(max_length=100L)
    pais = models.CharField(max_length=40L)
    cv_invitado = models.CharField(max_length=100L, blank=True)
    carta_aceptacion = models.CharField(max_length=100L, blank=True)
    class Meta:
        db_table = 'Accse_invitado'

class AccseSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    convocatoria = models.ForeignKey(AccseConvocatoria)
    propietario = models.ForeignKey('GrupoinvestInvestigador')
    fecha_presentacion = models.DateField()
    titulo_curso = models.TextField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    numero_asistentes = models.IntegerField()
    presupuesto_total = models.IntegerField()
    cantidad_solicitada = models.FloatField(null=True, blank=True)
    cofinanciacion_aportada = models.FloatField(null=True, blank=True)
    entidades_cofinanciadoras = models.TextField(blank=True)
    programa = models.CharField(max_length=100L, blank=True)
    aval = models.CharField(max_length=100L, blank=True)
    rechazar_condiciones = models.IntegerField()
    otra_solicitud = models.IntegerField()
    memoria = models.CharField(max_length=100L, blank=True)
    proyecto_investigacion = models.ForeignKey('ProyinvestProyectoinvestigacion', null=True, blank=True)
    cv_solicitante = models.CharField(max_length=100L, blank=True)
    class Meta:
        db_table = 'Accse_solicitud'

class AccseSolicitudGruposInteresados(models.Model):
    id = models.IntegerField(primary_key=True)
    solicitud = models.ForeignKey(AccseSolicitud)
    grupoinves = models.ForeignKey('GrupoinvestGrupoinves')
    class Meta:
        db_table = 'Accse_solicitud_grupos_interesados'

class AepinvuConvocatoria(models.Model):
    id = models.IntegerField(primary_key=True)
    num_convocatoria = models.IntegerField()
    fecha_inicio_aplicacion = models.DateField()
    fecha_final_aplicacion = models.DateField()
    fecha_inicio_presentacion = models.DateField()
    fecha_final_presentacion = models.DateField()
    fecha_inicio_validacion = models.DateField()
    fecha_fin_validacion = models.DateField()
    fecha_inicio_autorizacion = models.DateField()
    fecha_final_autorizacion = models.DateField()
    fecha_apertura_convocatoria = models.DateField(null=True, blank=True)
    fecha_cierre_convocatoria = models.DateField(null=True, blank=True)
    notificada = models.IntegerField(null=True, blank=True)
    resolucion_provisional = models.DateTimeField(null=True, blank=True)
    resolucion_definitiva = models.DateTimeField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    plazo_justificacion = models.IntegerField(null=True, blank=True)
    tipo_convocatoria = models.CharField(max_length=30L, blank=True)
    class Meta:
        db_table = 'Aepinvu_convocatoria'

class AepinvuEstadosolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    confirmada = models.IntegerField()
    rectificada = models.IntegerField()
    cancelada = models.IntegerField()
    valorada = models.IntegerField()
    concedida = models.IntegerField()
    desestimada = models.IntegerField()
    reclamada = models.IntegerField()
    renunciada = models.IntegerField()
    justificada = models.IntegerField(null=True, blank=True)
    archivada = models.IntegerField()
    anio = models.IntegerField()
    plazo = models.CharField(max_length=30L)
    propuesta = models.CharField(max_length=30L, blank=True)
    resolucion = models.CharField(max_length=30L)
    cantidad_concedida = models.FloatField(null=True, blank=True)
    razon_desestimacion = models.TextField(blank=True)
    observaciones_val = models.TextField(blank=True)
    observaciones_aut = models.TextField(blank=True)
    observaciones_int = models.TextField(blank=True)
    historial_comm = models.TextField(blank=True)
    notificado_inicio_justificacion = models.IntegerField()
    momento_creacion = models.DateTimeField(null=True, blank=True)
    fecha_registro_entrada = models.DateField(null=True, blank=True)
    momento_registro_entrada = models.DateTimeField(null=True, blank=True)
    fecha_limite_rectificacion = models.DateField(null=True, blank=True)
    momento_rectificacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_aceptacion = models.DateField(null=True, blank=True)
    fecha_carta_aceptacion = models.DateField(null=True, blank=True)
    momento_carta_aceptacion = models.DateTimeField(null=True, blank=True)
    momento_renuncia = models.DateTimeField(null=True, blank=True)
    momento_cancelacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_reclamacion = models.DateField(null=True, blank=True)
    momento_reclamacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_justificacion = models.DateField(null=True, blank=True)
    momento_justificacion = models.DateTimeField(null=True, blank=True)
    fichero_registro_entrada = models.CharField(max_length=100L, blank=True)
    fichero_carta_aceptacion = models.CharField(max_length=100L, blank=True)
    solicitud = models.ForeignKey('AepinvuSolicitud')
    class Meta:
        db_table = 'Aepinvu_estadosolicitud'

class AepinvuFilejustificacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AepinvuSolicitud')
    class Meta:
        db_table = 'Aepinvu_filejustificacion'

class AepinvuFilereclamacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AepinvuSolicitud')
    class Meta:
        db_table = 'Aepinvu_filereclamacion'

class AepinvuFilesubsanacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AepinvuSolicitud')
    class Meta:
        db_table = 'Aepinvu_filesubsanacion'

class AepinvuSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    convocatoria = models.ForeignKey(AepinvuConvocatoria)
    propietario = models.ForeignKey('GrupoinvestInvestigador')
    fecha_presentacion = models.DateField()
    primer_apellido = models.TextField()
    segundo_apellido = models.TextField(blank=True)
    nombre = models.TextField()
    nif = models.CharField(max_length=60L)
    categoria = models.TextField()
    centro_trabajo = models.TextField()
    direccion_postal = models.TextField()
    region_pais_origen = models.CharField(max_length=200L)
    email = models.CharField(max_length=60L)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    cv_invitado = models.CharField(max_length=100L, blank=True)
    carta_aceptacion = models.CharField(max_length=100L, blank=True)
    comunicacion = models.CharField(max_length=100L, blank=True)
    justificacion = models.CharField(max_length=100L, blank=True)
    rechazar_condiciones = models.IntegerField()
    cv = models.CharField(max_length=100L, blank=True)
    memoria = models.CharField(max_length=100L, blank=True)
    class Meta:
        db_table = 'Aepinvu_solicitud'

class AmgcConvocatoria(models.Model):
    id = models.IntegerField(primary_key=True)
    num_convocatoria = models.IntegerField()
    fecha_inicio_aplicacion = models.DateField()
    fecha_final_aplicacion = models.DateField()
    fecha_inicio_presentacion = models.DateField()
    fecha_final_presentacion = models.DateField()
    fecha_inicio_validacion = models.DateField()
    fecha_fin_validacion = models.DateField()
    fecha_inicio_autorizacion = models.DateField()
    fecha_final_autorizacion = models.DateField()
    fecha_apertura_convocatoria = models.DateField(null=True, blank=True)
    fecha_cierre_convocatoria = models.DateField(null=True, blank=True)
    notificada = models.IntegerField(null=True, blank=True)
    resolucion_provisional = models.DateTimeField(null=True, blank=True)
    resolucion_definitiva = models.DateTimeField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    plazo_justificacion = models.IntegerField(null=True, blank=True)
    tipo_convocatoria = models.CharField(max_length=30L, blank=True)
    class Meta:
        db_table = 'Amgc_convocatoria'

class AmgcEstadosolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    confirmada = models.IntegerField()
    rectificada = models.IntegerField()
    cancelada = models.IntegerField()
    valorada = models.IntegerField()
    concedida = models.IntegerField()
    desestimada = models.IntegerField()
    reclamada = models.IntegerField()
    renunciada = models.IntegerField()
    justificada = models.IntegerField(null=True, blank=True)
    archivada = models.IntegerField()
    anio = models.IntegerField()
    plazo = models.CharField(max_length=30L)
    propuesta = models.CharField(max_length=30L, blank=True)
    resolucion = models.CharField(max_length=30L)
    cantidad_concedida = models.FloatField(null=True, blank=True)
    razon_desestimacion = models.TextField(blank=True)
    observaciones_val = models.TextField(blank=True)
    observaciones_aut = models.TextField(blank=True)
    observaciones_int = models.TextField(blank=True)
    historial_comm = models.TextField(blank=True)
    notificado_inicio_justificacion = models.IntegerField()
    momento_creacion = models.DateTimeField(null=True, blank=True)
    fecha_registro_entrada = models.DateField(null=True, blank=True)
    momento_registro_entrada = models.DateTimeField(null=True, blank=True)
    fecha_limite_rectificacion = models.DateField(null=True, blank=True)
    momento_rectificacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_aceptacion = models.DateField(null=True, blank=True)
    fecha_carta_aceptacion = models.DateField(null=True, blank=True)
    momento_carta_aceptacion = models.DateTimeField(null=True, blank=True)
    momento_renuncia = models.DateTimeField(null=True, blank=True)
    momento_cancelacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_reclamacion = models.DateField(null=True, blank=True)
    momento_reclamacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_justificacion = models.DateField(null=True, blank=True)
    momento_justificacion = models.DateTimeField(null=True, blank=True)
    fichero_registro_entrada = models.CharField(max_length=100L, blank=True)
    fichero_carta_aceptacion = models.CharField(max_length=100L, blank=True)
    solicitud = models.ForeignKey('AmgcSolicitud')
    class Meta:
        db_table = 'Amgc_estadosolicitud'

class AmgcFilejustificacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AmgcSolicitud')
    class Meta:
        db_table = 'Amgc_filejustificacion'

class AmgcFilereclamacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AmgcSolicitud')
    class Meta:
        db_table = 'Amgc_filereclamacion'

class AmgcFilesubsanacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AmgcSolicitud')
    class Meta:
        db_table = 'Amgc_filesubsanacion'

class AmgcSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    convocatoria = models.ForeignKey(AmgcConvocatoria)
    propietario = models.ForeignKey('GrupoinvestInvestigador')
    fecha_presentacion = models.DateField()
    grupo = models.ForeignKey('GrupoinvestGrupoinves')
    cantidad_solicitada = models.FloatField(null=True, blank=True)
    memoria = models.CharField(max_length=100L, blank=True)
    proyectos_anteriores = models.TextField(blank=True)
    rechazar_condiciones = models.IntegerField()
    class Meta:
        db_table = 'Amgc_solicitud'

class AmgcSolicitudProyectos(models.Model):
    id = models.IntegerField(primary_key=True)
    solicitud = models.ForeignKey(AmgcSolicitud)
    proyectoinvestigacion = models.ForeignKey('ProyinvestProyectoinvestigacion')
    class Meta:
        db_table = 'Amgc_solicitud_proyectos'

class AmgcSolicitudProyectosSigidi(models.Model):
    id = models.IntegerField(primary_key=True)
    solicitud = models.ForeignKey(AmgcSolicitud)
    proyectosigidi = models.ForeignKey('ProyinvestProyectosigidi')
    class Meta:
        db_table = 'Amgc_solicitud_proyectos_sigidi'

class AocrcConvocatoria(models.Model):
    id = models.IntegerField(primary_key=True)
    num_convocatoria = models.IntegerField()
    fecha_inicio_aplicacion = models.DateField()
    fecha_final_aplicacion = models.DateField()
    fecha_inicio_presentacion = models.DateField()
    fecha_final_presentacion = models.DateField()
    fecha_inicio_validacion = models.DateField()
    fecha_fin_validacion = models.DateField()
    fecha_inicio_autorizacion = models.DateField()
    fecha_final_autorizacion = models.DateField()
    fecha_apertura_convocatoria = models.DateField(null=True, blank=True)
    fecha_cierre_convocatoria = models.DateField(null=True, blank=True)
    notificada = models.IntegerField(null=True, blank=True)
    resolucion_provisional = models.DateTimeField(null=True, blank=True)
    resolucion_definitiva = models.DateTimeField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    plazo_justificacion = models.IntegerField(null=True, blank=True)
    tipo_convocatoria = models.CharField(max_length=30L, blank=True)
    class Meta:
        db_table = 'Aocrc_convocatoria'

class AocrcEstadosolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    confirmada = models.IntegerField()
    rectificada = models.IntegerField()
    cancelada = models.IntegerField()
    valorada = models.IntegerField()
    concedida = models.IntegerField()
    desestimada = models.IntegerField()
    reclamada = models.IntegerField()
    renunciada = models.IntegerField()
    justificada = models.IntegerField(null=True, blank=True)
    archivada = models.IntegerField()
    anio = models.IntegerField()
    plazo = models.CharField(max_length=30L)
    propuesta = models.CharField(max_length=30L, blank=True)
    resolucion = models.CharField(max_length=30L)
    cantidad_concedida = models.FloatField(null=True, blank=True)
    razon_desestimacion = models.TextField(blank=True)
    observaciones_val = models.TextField(blank=True)
    observaciones_aut = models.TextField(blank=True)
    observaciones_int = models.TextField(blank=True)
    historial_comm = models.TextField(blank=True)
    notificado_inicio_justificacion = models.IntegerField()
    momento_creacion = models.DateTimeField(null=True, blank=True)
    fecha_registro_entrada = models.DateField(null=True, blank=True)
    momento_registro_entrada = models.DateTimeField(null=True, blank=True)
    fecha_limite_rectificacion = models.DateField(null=True, blank=True)
    momento_rectificacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_aceptacion = models.DateField(null=True, blank=True)
    fecha_carta_aceptacion = models.DateField(null=True, blank=True)
    momento_carta_aceptacion = models.DateTimeField(null=True, blank=True)
    momento_renuncia = models.DateTimeField(null=True, blank=True)
    momento_cancelacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_reclamacion = models.DateField(null=True, blank=True)
    momento_reclamacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_justificacion = models.DateField(null=True, blank=True)
    momento_justificacion = models.DateTimeField(null=True, blank=True)
    fichero_registro_entrada = models.CharField(max_length=100L, blank=True)
    fichero_carta_aceptacion = models.CharField(max_length=100L, blank=True)
    solicitud = models.ForeignKey('AocrcSolicitud')
    class Meta:
        db_table = 'Aocrc_estadosolicitud'

class AocrcFilejustificacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AocrcSolicitud')
    class Meta:
        db_table = 'Aocrc_filejustificacion'

class AocrcFilereclamacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AocrcSolicitud')
    class Meta:
        db_table = 'Aocrc_filereclamacion'

class AocrcFilesubsanacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AocrcSolicitud')
    class Meta:
        db_table = 'Aocrc_filesubsanacion'

class AocrcMotivoviaje(models.Model):
    id = models.IntegerField(primary_key=True)
    motivo = models.CharField(max_length=50L)
    class Meta:
        db_table = 'Aocrc_motivoviaje'

class AocrcSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    convocatoria = models.ForeignKey(AocrcConvocatoria)
    propietario = models.ForeignKey('GrupoinvestInvestigador')
    fecha_presentacion = models.DateField()
    nombre_congreso = models.TextField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    numero_asistentes = models.IntegerField()
    presupuesto = models.FloatField()
    cantidad_solicitada = models.FloatField(null=True, blank=True)
    cofinanciacion = models.FloatField()
    entidad_cofinanciadora = models.TextField(blank=True)
    aval = models.CharField(max_length=100L, blank=True)
    justificacion = models.CharField(max_length=100L, blank=True)
    rechazar_condiciones = models.IntegerField()
    memoria = models.CharField(max_length=100L, blank=True)
    class Meta:
        db_table = 'Aocrc_solicitud'

class AocrcSolicitudGrupos(models.Model):
    id = models.IntegerField(primary_key=True)
    solicitud = models.ForeignKey(AocrcSolicitud)
    grupoinves = models.ForeignKey('GrupoinvestGrupoinves')
    class Meta:
        db_table = 'Aocrc_solicitud_grupos'

class ArtddConvocatoria(models.Model):
    id = models.IntegerField(primary_key=True)
    num_convocatoria = models.IntegerField()
    fecha_inicio_aplicacion = models.DateField()
    fecha_final_aplicacion = models.DateField()
    fecha_inicio_presentacion = models.DateField()
    fecha_final_presentacion = models.DateField()
    fecha_inicio_validacion = models.DateField()
    fecha_fin_validacion = models.DateField()
    fecha_inicio_autorizacion = models.DateField()
    fecha_final_autorizacion = models.DateField()
    fecha_apertura_convocatoria = models.DateField(null=True, blank=True)
    fecha_cierre_convocatoria = models.DateField(null=True, blank=True)
    notificada = models.IntegerField(null=True, blank=True)
    resolucion_provisional = models.DateTimeField(null=True, blank=True)
    resolucion_definitiva = models.DateTimeField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    plazo_justificacion = models.IntegerField(null=True, blank=True)
    tipo_convocatoria = models.CharField(max_length=30L, blank=True)
    class Meta:
        db_table = 'Artdd_convocatoria'

class ArtddEstadosolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    confirmada = models.IntegerField()
    rectificada = models.IntegerField()
    cancelada = models.IntegerField()
    valorada = models.IntegerField()
    concedida = models.IntegerField()
    desestimada = models.IntegerField()
    reclamada = models.IntegerField()
    renunciada = models.IntegerField()
    justificada = models.IntegerField(null=True, blank=True)
    archivada = models.IntegerField()
    anio = models.IntegerField()
    plazo = models.CharField(max_length=30L)
    propuesta = models.CharField(max_length=30L, blank=True)
    resolucion = models.CharField(max_length=30L)
    cantidad_concedida = models.FloatField(null=True, blank=True)
    razon_desestimacion = models.TextField(blank=True)
    observaciones_val = models.TextField(blank=True)
    observaciones_aut = models.TextField(blank=True)
    observaciones_int = models.TextField(blank=True)
    historial_comm = models.TextField(blank=True)
    notificado_inicio_justificacion = models.IntegerField()
    momento_creacion = models.DateTimeField(null=True, blank=True)
    fecha_registro_entrada = models.DateField(null=True, blank=True)
    momento_registro_entrada = models.DateTimeField(null=True, blank=True)
    fecha_limite_rectificacion = models.DateField(null=True, blank=True)
    momento_rectificacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_aceptacion = models.DateField(null=True, blank=True)
    fecha_carta_aceptacion = models.DateField(null=True, blank=True)
    momento_carta_aceptacion = models.DateTimeField(null=True, blank=True)
    momento_renuncia = models.DateTimeField(null=True, blank=True)
    momento_cancelacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_reclamacion = models.DateField(null=True, blank=True)
    momento_reclamacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_justificacion = models.DateField(null=True, blank=True)
    momento_justificacion = models.DateTimeField(null=True, blank=True)
    fichero_registro_entrada = models.CharField(max_length=100L, blank=True)
    fichero_carta_aceptacion = models.CharField(max_length=100L, blank=True)
    solicitud = models.ForeignKey('ArtddSolicitud')
    class Meta:
        db_table = 'Artdd_estadosolicitud'

class ArtddFilejustificacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('ArtddSolicitud')
    class Meta:
        db_table = 'Artdd_filejustificacion'

class ArtddFilereclamacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('ArtddSolicitud')
    class Meta:
        db_table = 'Artdd_filereclamacion'

class ArtddFilesubsanacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('ArtddSolicitud')
    class Meta:
        db_table = 'Artdd_filesubsanacion'

class ArtddSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    convocatoria = models.ForeignKey(ArtddConvocatoria)
    propietario = models.ForeignKey('GrupoinvestInvestigador')
    fecha_presentacion = models.DateField()
    objeto_desplazamiento = models.TextField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    dias_estancia = models.IntegerField()
    institucion_destino = models.TextField()
    ciudad = models.TextField()
    pais = models.TextField()
    fecha_lectura = models.DateField()
    acreditacion_tesis = models.CharField(max_length=100L, blank=True)
    aceptacion = models.CharField(max_length=100L, blank=True)
    memoria_previa = models.CharField(max_length=100L, blank=True)
    memoria_final = models.CharField(max_length=100L, blank=True)
    rechazar_condiciones = models.IntegerField()
    acreditacion_dea = models.CharField(max_length=100L, blank=True)
    class Meta:
        db_table = 'Artdd_solicitud'

class ArtdmConvocatoria(models.Model):
    id = models.IntegerField(primary_key=True)
    num_convocatoria = models.IntegerField()
    fecha_inicio_aplicacion = models.DateField()
    fecha_final_aplicacion = models.DateField()
    fecha_inicio_presentacion = models.DateField()
    fecha_final_presentacion = models.DateField()
    fecha_inicio_validacion = models.DateField()
    fecha_fin_validacion = models.DateField()
    fecha_inicio_autorizacion = models.DateField()
    fecha_final_autorizacion = models.DateField()
    fecha_apertura_convocatoria = models.DateField(null=True, blank=True)
    fecha_cierre_convocatoria = models.DateField(null=True, blank=True)
    notificada = models.IntegerField(null=True, blank=True)
    resolucion_provisional = models.DateTimeField(null=True, blank=True)
    resolucion_definitiva = models.DateTimeField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    plazo_justificacion = models.IntegerField(null=True, blank=True)
    tipo_convocatoria = models.CharField(max_length=30L, blank=True)
    class Meta:
        db_table = 'Artdm_convocatoria'

class ArtdmEstadosolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    confirmada = models.IntegerField()
    rectificada = models.IntegerField()
    cancelada = models.IntegerField()
    valorada = models.IntegerField()
    concedida = models.IntegerField()
    desestimada = models.IntegerField()
    reclamada = models.IntegerField()
    renunciada = models.IntegerField()
    justificada = models.IntegerField(null=True, blank=True)
    archivada = models.IntegerField()
    anio = models.IntegerField()
    plazo = models.CharField(max_length=30L)
    propuesta = models.CharField(max_length=30L, blank=True)
    resolucion = models.CharField(max_length=30L)
    cantidad_concedida = models.FloatField(null=True, blank=True)
    razon_desestimacion = models.TextField(blank=True)
    observaciones_val = models.TextField(blank=True)
    observaciones_aut = models.TextField(blank=True)
    observaciones_int = models.TextField(blank=True)
    historial_comm = models.TextField(blank=True)
    notificado_inicio_justificacion = models.IntegerField()
    momento_creacion = models.DateTimeField(null=True, blank=True)
    fecha_registro_entrada = models.DateField(null=True, blank=True)
    momento_registro_entrada = models.DateTimeField(null=True, blank=True)
    fecha_limite_rectificacion = models.DateField(null=True, blank=True)
    momento_rectificacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_aceptacion = models.DateField(null=True, blank=True)
    fecha_carta_aceptacion = models.DateField(null=True, blank=True)
    momento_carta_aceptacion = models.DateTimeField(null=True, blank=True)
    momento_renuncia = models.DateTimeField(null=True, blank=True)
    momento_cancelacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_reclamacion = models.DateField(null=True, blank=True)
    momento_reclamacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_justificacion = models.DateField(null=True, blank=True)
    momento_justificacion = models.DateTimeField(null=True, blank=True)
    fichero_registro_entrada = models.CharField(max_length=100L, blank=True)
    fichero_carta_aceptacion = models.CharField(max_length=100L, blank=True)
    solicitud = models.ForeignKey('ArtdmSolicitud')
    class Meta:
        db_table = 'Artdm_estadosolicitud'

class ArtdmFilejustificacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('ArtdmSolicitud')
    class Meta:
        db_table = 'Artdm_filejustificacion'

class ArtdmFilereclamacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('ArtdmSolicitud')
    class Meta:
        db_table = 'Artdm_filereclamacion'

class ArtdmFilesubsanacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('ArtdmSolicitud')
    class Meta:
        db_table = 'Artdm_filesubsanacion'

class ArtdmSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    convocatoria = models.ForeignKey(ArtdmConvocatoria)
    propietario = models.ForeignKey('GrupoinvestInvestigador')
    fecha_presentacion = models.DateField()
    material = models.TextField()
    importe = models.FloatField()
    fecha_lectura = models.DateField()
    acreditacion_tesis = models.CharField(max_length=100L, blank=True)
    facturas = models.CharField(max_length=100L, blank=True)
    rechazar_condiciones = models.IntegerField()
    acreditacion_dea = models.CharField(max_length=100L, blank=True)
    class Meta:
        db_table = 'Artdm_solicitud'

class AyudahumanidadesConvocatoria(models.Model):
    id = models.IntegerField(primary_key=True)
    num_convocatoria = models.IntegerField()
    fecha_inicio_aplicacion = models.DateField()
    fecha_final_aplicacion = models.DateField()
    fecha_inicio_presentacion = models.DateField()
    fecha_final_presentacion = models.DateField()
    fecha_inicio_validacion = models.DateField()
    fecha_fin_validacion = models.DateField()
    fecha_inicio_autorizacion = models.DateField()
    fecha_final_autorizacion = models.DateField()
    fecha_apertura_convocatoria = models.DateField(null=True, blank=True)
    fecha_cierre_convocatoria = models.DateField(null=True, blank=True)
    notificada = models.IntegerField(null=True, blank=True)
    resolucion_provisional = models.DateTimeField(null=True, blank=True)
    resolucion_definitiva = models.DateTimeField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    plazo_justificacion = models.IntegerField(null=True, blank=True)
    tipo_convocatoria = models.CharField(max_length=30L, blank=True)
    class Meta:
        db_table = 'AyudaHumanidades_convocatoria'

class AyudahumanidadesEstadosolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    confirmada = models.IntegerField()
    rectificada = models.IntegerField()
    cancelada = models.IntegerField()
    valorada = models.IntegerField()
    concedida = models.IntegerField()
    desestimada = models.IntegerField()
    reclamada = models.IntegerField()
    renunciada = models.IntegerField()
    justificada = models.IntegerField(null=True, blank=True)
    archivada = models.IntegerField()
    anio = models.IntegerField()
    plazo = models.CharField(max_length=30L)
    propuesta = models.CharField(max_length=30L, blank=True)
    resolucion = models.CharField(max_length=30L)
    cantidad_concedida = models.FloatField(null=True, blank=True)
    razon_desestimacion = models.TextField(blank=True)
    observaciones_val = models.TextField(blank=True)
    observaciones_aut = models.TextField(blank=True)
    observaciones_int = models.TextField(blank=True)
    historial_comm = models.TextField(blank=True)
    notificado_inicio_justificacion = models.IntegerField()
    momento_creacion = models.DateTimeField(null=True, blank=True)
    fecha_registro_entrada = models.DateField(null=True, blank=True)
    momento_registro_entrada = models.DateTimeField(null=True, blank=True)
    fecha_limite_rectificacion = models.DateField(null=True, blank=True)
    momento_rectificacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_aceptacion = models.DateField(null=True, blank=True)
    fecha_carta_aceptacion = models.DateField(null=True, blank=True)
    momento_carta_aceptacion = models.DateTimeField(null=True, blank=True)
    momento_renuncia = models.DateTimeField(null=True, blank=True)
    momento_cancelacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_reclamacion = models.DateField(null=True, blank=True)
    momento_reclamacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_justificacion = models.DateField(null=True, blank=True)
    momento_justificacion = models.DateTimeField(null=True, blank=True)
    fichero_registro_entrada = models.CharField(max_length=100L, blank=True)
    fichero_carta_aceptacion = models.CharField(max_length=100L, blank=True)
    solicitud = models.ForeignKey('AyudahumanidadesSolicitud')
    class Meta:
        db_table = 'AyudaHumanidades_estadosolicitud'

class AyudahumanidadesFileconfirmation(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudahumanidadesSolicitud')
    class Meta:
        db_table = 'AyudaHumanidades_fileconfirmation'

class AyudahumanidadesFilecvnteam(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudahumanidadesSolicitud')
    class Meta:
        db_table = 'AyudaHumanidades_filecvnteam'

class AyudahumanidadesFilejustificacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudahumanidadesSolicitud')
    class Meta:
        db_table = 'AyudaHumanidades_filejustificacion'

class AyudahumanidadesFilereclamacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudahumanidadesSolicitud')
    class Meta:
        db_table = 'AyudaHumanidades_filereclamacion'

class AyudahumanidadesFilesubsanacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudahumanidadesSolicitud')
    class Meta:
        db_table = 'AyudaHumanidades_filesubsanacion'

class AyudahumanidadesSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    convocatoria = models.ForeignKey(AyudahumanidadesConvocatoria)
    propietario = models.ForeignKey('GrupoinvestInvestigador')
    fecha_presentacion = models.DateField()
    titulo_proyecto = models.TextField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    memoria_descrip = models.CharField(max_length=100L, blank=True)
    cantidad_solicitada = models.FloatField()
    compromiso_proyecto = models.CharField(max_length=100L, blank=True)
    declaracion_responsable = models.IntegerField()
    no_part_proyecto = models.IntegerField()
    rechazar_condiciones = models.IntegerField()
    class Meta:
        db_table = 'AyudaHumanidades_solicitud'

class AyudahumanidadesSolicitudEquipo(models.Model):
    id = models.IntegerField(primary_key=True)
    solicitud = models.ForeignKey(AyudahumanidadesSolicitud)
    investigador = models.ForeignKey('GrupoinvestInvestigador')
    class Meta:
        db_table = 'AyudaHumanidades_solicitud_equipo'

class AyudainiciacionConvocatoria(models.Model):
    id = models.IntegerField(primary_key=True)
    num_convocatoria = models.IntegerField()
    fecha_inicio_aplicacion = models.DateField()
    fecha_final_aplicacion = models.DateField()
    fecha_inicio_presentacion = models.DateField()
    fecha_final_presentacion = models.DateField()
    fecha_inicio_validacion = models.DateField()
    fecha_fin_validacion = models.DateField()
    fecha_inicio_autorizacion = models.DateField()
    fecha_final_autorizacion = models.DateField()
    fecha_apertura_convocatoria = models.DateField(null=True, blank=True)
    fecha_cierre_convocatoria = models.DateField(null=True, blank=True)
    notificada = models.IntegerField(null=True, blank=True)
    resolucion_provisional = models.DateTimeField(null=True, blank=True)
    resolucion_definitiva = models.DateTimeField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    plazo_justificacion = models.IntegerField(null=True, blank=True)
    tipo_convocatoria = models.CharField(max_length=30L, blank=True)
    class Meta:
        db_table = 'AyudaIniciacion_convocatoria'

class AyudainiciacionEstadosolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    confirmada = models.IntegerField()
    rectificada = models.IntegerField()
    cancelada = models.IntegerField()
    valorada = models.IntegerField()
    concedida = models.IntegerField()
    desestimada = models.IntegerField()
    reclamada = models.IntegerField()
    renunciada = models.IntegerField()
    justificada = models.IntegerField(null=True, blank=True)
    archivada = models.IntegerField()
    anio = models.IntegerField()
    plazo = models.CharField(max_length=30L)
    propuesta = models.CharField(max_length=30L, blank=True)
    resolucion = models.CharField(max_length=30L)
    cantidad_concedida = models.FloatField(null=True, blank=True)
    razon_desestimacion = models.TextField(blank=True)
    observaciones_val = models.TextField(blank=True)
    observaciones_aut = models.TextField(blank=True)
    observaciones_int = models.TextField(blank=True)
    historial_comm = models.TextField(blank=True)
    notificado_inicio_justificacion = models.IntegerField()
    momento_creacion = models.DateTimeField(null=True, blank=True)
    fecha_registro_entrada = models.DateField(null=True, blank=True)
    momento_registro_entrada = models.DateTimeField(null=True, blank=True)
    fecha_limite_rectificacion = models.DateField(null=True, blank=True)
    momento_rectificacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_aceptacion = models.DateField(null=True, blank=True)
    fecha_carta_aceptacion = models.DateField(null=True, blank=True)
    momento_carta_aceptacion = models.DateTimeField(null=True, blank=True)
    momento_renuncia = models.DateTimeField(null=True, blank=True)
    momento_cancelacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_reclamacion = models.DateField(null=True, blank=True)
    momento_reclamacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_justificacion = models.DateField(null=True, blank=True)
    momento_justificacion = models.DateTimeField(null=True, blank=True)
    fichero_registro_entrada = models.CharField(max_length=100L, blank=True)
    fichero_carta_aceptacion = models.CharField(max_length=100L, blank=True)
    solicitud = models.ForeignKey('AyudainiciacionSolicitud')
    class Meta:
        db_table = 'AyudaIniciacion_estadosolicitud'

class AyudainiciacionFileconfirmation(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudainiciacionSolicitud')
    class Meta:
        db_table = 'AyudaIniciacion_fileconfirmation'

class AyudainiciacionFilecvnteam(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudainiciacionSolicitud')
    class Meta:
        db_table = 'AyudaIniciacion_filecvnteam'

class AyudainiciacionFilejustificacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudainiciacionSolicitud')
    class Meta:
        db_table = 'AyudaIniciacion_filejustificacion'

class AyudainiciacionFilereclamacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudainiciacionSolicitud')
    class Meta:
        db_table = 'AyudaIniciacion_filereclamacion'

class AyudainiciacionFilesubsanacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudainiciacionSolicitud')
    class Meta:
        db_table = 'AyudaIniciacion_filesubsanacion'

class AyudainiciacionSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    convocatoria = models.ForeignKey(AyudainiciacionConvocatoria)
    propietario = models.ForeignKey('GrupoinvestInvestigador')
    fecha_presentacion = models.DateField()
    titulo_proyecto = models.TextField()
    fecha_nacimiento = models.DateField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    memoria_descrip = models.CharField(max_length=100L, blank=True)
    cantidad_solicitada = models.FloatField()
    compromiso = models.IntegerField()
    compromiso_proyecto = models.CharField(max_length=100L, blank=True)
    declaracion_responsable = models.IntegerField()
    no_part_proyecto = models.IntegerField()
    rechazar_condiciones = models.IntegerField()
    class Meta:
        db_table = 'AyudaIniciacion_solicitud'

class AyudainiciacionSolicitudEquipo(models.Model):
    id = models.IntegerField(primary_key=True)
    solicitud = models.ForeignKey(AyudainiciacionSolicitud)
    investigador = models.ForeignKey('GrupoinvestInvestigador')
    class Meta:
        db_table = 'AyudaIniciacion_solicitud_equipo'

class AyudapuenteConvocatoria(models.Model):
    id = models.IntegerField(primary_key=True)
    num_convocatoria = models.IntegerField()
    fecha_inicio_aplicacion = models.DateField()
    fecha_final_aplicacion = models.DateField()
    fecha_inicio_presentacion = models.DateField()
    fecha_final_presentacion = models.DateField()
    fecha_inicio_validacion = models.DateField()
    fecha_fin_validacion = models.DateField()
    fecha_inicio_autorizacion = models.DateField()
    fecha_final_autorizacion = models.DateField()
    fecha_apertura_convocatoria = models.DateField(null=True, blank=True)
    fecha_cierre_convocatoria = models.DateField(null=True, blank=True)
    notificada = models.IntegerField(null=True, blank=True)
    resolucion_provisional = models.DateTimeField(null=True, blank=True)
    resolucion_definitiva = models.DateTimeField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    plazo_justificacion = models.IntegerField(null=True, blank=True)
    tipo_convocatoria = models.CharField(max_length=30L, blank=True)
    class Meta:
        db_table = 'AyudaPuente_convocatoria'

class AyudapuenteEstadosolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    confirmada = models.IntegerField()
    rectificada = models.IntegerField()
    cancelada = models.IntegerField()
    valorada = models.IntegerField()
    concedida = models.IntegerField()
    desestimada = models.IntegerField()
    reclamada = models.IntegerField()
    renunciada = models.IntegerField()
    justificada = models.IntegerField(null=True, blank=True)
    archivada = models.IntegerField()
    anio = models.IntegerField()
    plazo = models.CharField(max_length=30L)
    propuesta = models.CharField(max_length=30L, blank=True)
    resolucion = models.CharField(max_length=30L)
    cantidad_concedida = models.FloatField(null=True, blank=True)
    razon_desestimacion = models.TextField(blank=True)
    observaciones_val = models.TextField(blank=True)
    observaciones_aut = models.TextField(blank=True)
    observaciones_int = models.TextField(blank=True)
    historial_comm = models.TextField(blank=True)
    notificado_inicio_justificacion = models.IntegerField()
    momento_creacion = models.DateTimeField(null=True, blank=True)
    fecha_registro_entrada = models.DateField(null=True, blank=True)
    momento_registro_entrada = models.DateTimeField(null=True, blank=True)
    fecha_limite_rectificacion = models.DateField(null=True, blank=True)
    momento_rectificacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_aceptacion = models.DateField(null=True, blank=True)
    fecha_carta_aceptacion = models.DateField(null=True, blank=True)
    momento_carta_aceptacion = models.DateTimeField(null=True, blank=True)
    momento_renuncia = models.DateTimeField(null=True, blank=True)
    momento_cancelacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_reclamacion = models.DateField(null=True, blank=True)
    momento_reclamacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_justificacion = models.DateField(null=True, blank=True)
    momento_justificacion = models.DateTimeField(null=True, blank=True)
    fichero_registro_entrada = models.CharField(max_length=100L, blank=True)
    fichero_carta_aceptacion = models.CharField(max_length=100L, blank=True)
    solicitud = models.ForeignKey('AyudapuenteSolicitud')
    class Meta:
        db_table = 'AyudaPuente_estadosolicitud'

class AyudapuenteFilejustificacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudapuenteSolicitud')
    class Meta:
        db_table = 'AyudaPuente_filejustificacion'

class AyudapuenteFilereclamacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudapuenteSolicitud')
    class Meta:
        db_table = 'AyudaPuente_filereclamacion'

class AyudapuenteFilesubsanacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('AyudapuenteSolicitud')
    class Meta:
        db_table = 'AyudaPuente_filesubsanacion'

class AyudapuenteSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    convocatoria = models.ForeignKey(AyudapuenteConvocatoria)
    propietario = models.ForeignKey('GrupoinvestInvestigador')
    fecha_presentacion = models.DateField()
    titulo_proyecto = models.TextField()
    organismo_convocante = models.TextField()
    cantidad_solicitada = models.FloatField()
    fecha_publicacion_boe = models.DateField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    proyecto = models.CharField(max_length=100L, blank=True)
    comunicacion_ministerio = models.CharField(max_length=100L, blank=True)
    informe_anep = models.CharField(max_length=100L, blank=True)
    compromiso = models.IntegerField()
    rechazar_condiciones = models.IntegerField()
    class Meta:
        db_table = 'AyudaPuente_solicitud'

class BolsaviajesConvocatoria(models.Model):
    id = models.IntegerField(primary_key=True)
    num_convocatoria = models.IntegerField()
    fecha_inicio_aplicacion = models.DateField()
    fecha_final_aplicacion = models.DateField()
    fecha_inicio_presentacion = models.DateField()
    fecha_final_presentacion = models.DateField()
    fecha_inicio_validacion = models.DateField()
    fecha_fin_validacion = models.DateField()
    fecha_inicio_autorizacion = models.DateField()
    fecha_final_autorizacion = models.DateField()
    fecha_apertura_convocatoria = models.DateField(null=True, blank=True)
    fecha_cierre_convocatoria = models.DateField(null=True, blank=True)
    notificada = models.IntegerField(null=True, blank=True)
    resolucion_provisional = models.DateTimeField(null=True, blank=True)
    resolucion_definitiva = models.DateTimeField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    plazo_justificacion = models.IntegerField(null=True, blank=True)
    tipo_convocatoria = models.CharField(max_length=30L, blank=True)
    class Meta:
        db_table = 'BolsaViajes_convocatoria'

class BolsaviajesEstadosolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    confirmada = models.IntegerField()
    rectificada = models.IntegerField()
    cancelada = models.IntegerField()
    valorada = models.IntegerField()
    concedida = models.IntegerField()
    desestimada = models.IntegerField()
    reclamada = models.IntegerField()
    renunciada = models.IntegerField()
    justificada = models.IntegerField(null=True, blank=True)
    archivada = models.IntegerField()
    anio = models.IntegerField()
    plazo = models.CharField(max_length=30L)
    propuesta = models.CharField(max_length=30L, blank=True)
    resolucion = models.CharField(max_length=30L)
    cantidad_concedida = models.FloatField(null=True, blank=True)
    razon_desestimacion = models.TextField(blank=True)
    observaciones_val = models.TextField(blank=True)
    observaciones_aut = models.TextField(blank=True)
    observaciones_int = models.TextField(blank=True)
    historial_comm = models.TextField(blank=True)
    notificado_inicio_justificacion = models.IntegerField()
    momento_creacion = models.DateTimeField(null=True, blank=True)
    fecha_registro_entrada = models.DateField(null=True, blank=True)
    momento_registro_entrada = models.DateTimeField(null=True, blank=True)
    fecha_limite_rectificacion = models.DateField(null=True, blank=True)
    momento_rectificacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_aceptacion = models.DateField(null=True, blank=True)
    fecha_carta_aceptacion = models.DateField(null=True, blank=True)
    momento_carta_aceptacion = models.DateTimeField(null=True, blank=True)
    momento_renuncia = models.DateTimeField(null=True, blank=True)
    momento_cancelacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_reclamacion = models.DateField(null=True, blank=True)
    momento_reclamacion = models.DateTimeField(null=True, blank=True)
    fecha_limite_justificacion = models.DateField(null=True, blank=True)
    momento_justificacion = models.DateTimeField(null=True, blank=True)
    fichero_registro_entrada = models.CharField(max_length=100L, blank=True)
    fichero_carta_aceptacion = models.CharField(max_length=100L, blank=True)
    solicitud = models.ForeignKey('BolsaviajesSolicitud')
    class Meta:
        db_table = 'BolsaViajes_estadosolicitud'

class BolsaviajesFilejustificacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('BolsaviajesSolicitud')
    class Meta:
        db_table = 'BolsaViajes_filejustificacion'

class BolsaviajesFilereclamacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('BolsaviajesSolicitud')
    class Meta:
        db_table = 'BolsaViajes_filereclamacion'

class BolsaviajesFilesubsanacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    solicitud = models.ForeignKey('BolsaviajesSolicitud')
    class Meta:
        db_table = 'BolsaViajes_filesubsanacion'

class BolsaviajesMotivoviaje(models.Model):
    id = models.IntegerField(primary_key=True)
    motivo = models.CharField(max_length=50L)
    class Meta:
        db_table = 'BolsaViajes_motivoviaje'

class BolsaviajesSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    convocatoria = models.ForeignKey(BolsaviajesConvocatoria)
    propietario = models.ForeignKey('GrupoinvestInvestigador')
    fecha_presentacion = models.DateField()
    motivo_viaje = models.ForeignKey(BolsaviajesMotivoviaje)
    nombre_congreso = models.TextField()
    nombre_comunicacion = models.TextField()
    autores = models.TextField()
    institucion_destino = models.TextField()
    ciudad_destino = models.TextField()
    pais_destino = models.TextField()
    region_pais_destino = models.CharField(max_length=200L)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    cantidad_solicitada = models.FloatField(null=True, blank=True)
    web = models.CharField(max_length=200L)
    programa_cientifico = models.CharField(max_length=100L, blank=True)
    abstract = models.CharField(max_length=100L, blank=True)
    dec_beneficiario = models.IntegerField()
    dec_incompatibilidad = models.IntegerField()
    rechazar_condiciones = models.IntegerField()
    otra_solicitud = models.IntegerField()
    memoria = models.CharField(max_length=100L, blank=True)
    proyecto_investigacion = models.ForeignKey('ProyinvestProyectoinvestigacion', null=True, blank=True)
    proyecto_investigacion_sigidi = models.ForeignKey('ProyinvestProyectosigidi', null=True, blank=True)
    class Meta:
        db_table = 'BolsaViajes_solicitud'

class CeibaAcreditacion(models.Model):
    id = models.IntegerField(primary_key=True)
    investigador = models.ForeignKey('GrupoinvestInvestigador', unique=True)
    nivel = models.CharField(max_length=2L)
    comentarios = models.TextField(blank=True)
    class Meta:
        db_table = 'Ceiba_acreditacion'

class CeibaEstado(models.Model):
    id = models.IntegerField(primary_key=True)
    solicitud = models.ForeignKey('CeibaSolicitud')
    borrador = models.IntegerField()
    presentado = models.IntegerField()
    pdte_ponente = models.IntegerField()
    redaccion = models.IntegerField()
    votacion = models.IntegerField()
    votacion_fin = models.IntegerField()
    pdte_reunion = models.IntegerField()
    aceptado = models.IntegerField()
    rechazado = models.IntegerField()
    cancelado = models.IntegerField()
    fecha_cambio = models.DateField()
    nombre = models.CharField(max_length=15L)
    mensaje = models.CharField(max_length=30L)
    class Meta:
        db_table = 'Ceiba_estado'

class CeibaFileinfoacreditacion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    item = models.ForeignKey(CeibaAcreditacion)
    class Meta:
        db_table = 'Ceiba_fileinfoacreditacion'

class CeibaFileinfocomision(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    item = models.ForeignKey('CeibaInforme')
    class Meta:
        db_table = 'Ceiba_fileinfocomision'

class CeibaFileinfoinvestigador(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200L)
    name = models.CharField(max_length=200L)
    ext = models.CharField(max_length=50L)
    url = models.CharField(max_length=255L)
    path = models.CharField(max_length=255L)
    date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    item = models.ForeignKey('CeibaSolicitud')
    class Meta:
        db_table = 'Ceiba_fileinfoinvestigador'

class CeibaInforme(models.Model):
    id = models.IntegerField(primary_key=True)
    estado = models.ForeignKey(CeibaEstado)
    ponente = models.ForeignKey('GrupoinvestInvestigador', null=True, blank=True)
    notas_internas = models.TextField(blank=True)
    informe = models.TextField(blank=True)
    dias_disponibles = models.IntegerField(null=True, blank=True)
    tiempo_informe = models.IntegerField(null=True, blank=True)
    fecha_acta_reunion = models.DateField(null=True, blank=True)
    fecha_salida = models.DateField(null=True, blank=True)
    files_add = models.IntegerField()
    files_down = models.IntegerField()
    files_del = models.IntegerField()
    class Meta:
        db_table = 'Ceiba_informe'

class CeibaInformeComision(models.Model):
    id = models.IntegerField(primary_key=True)
    informe = models.ForeignKey(CeibaInforme)
    investigador = models.ForeignKey('GrupoinvestInvestigador')
    class Meta:
        db_table = 'Ceiba_informe_comision'

class CeibaOrganismo(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50L)
    class Meta:
        db_table = 'Ceiba_organismo'

class CeibaSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.ForeignKey('GrupoinvestInvestigador')
    organismo = models.ForeignKey(CeibaOrganismo)
    titulo_proyecto = models.TextField()
    fecha_final = models.DateField()
    resumen = models.TextField()
    asuntos_eticos = models.TextField()
    inc_seres_humanos = models.IntegerField()
    inc_psico_humanos = models.IntegerField()
    inc_muestras_humanos = models.IntegerField()
    inc_animales_vivos = models.IntegerField()
    inc_animales_sacrif = models.IntegerField()
    inc_animales_otros = models.IntegerField()
    inc_otros = models.TextField(blank=True)
    comentarios = models.TextField(blank=True)
    numero_registro = models.CharField(max_length=30L, blank=True)
    fecha_creacion = models.DateField(null=True, blank=True)
    fecha_envio = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'Ceiba_solicitud'

class CeibaSolicitudMiembrosGrupo(models.Model):
    id = models.IntegerField(primary_key=True)
    solicitud = models.ForeignKey(CeibaSolicitud)
    investigador = models.ForeignKey('GrupoinvestInvestigador')
    class Meta:
        db_table = 'Ceiba_solicitud_miembros_grupo'

class CeibaVotacion(models.Model):
    id = models.IntegerField(primary_key=True)
    informe = models.ForeignKey(CeibaInforme)
    votante = models.ForeignKey('GrupoinvestInvestigador')
    voto = models.CharField(max_length=1L)
    fecha_voto = models.DateField(null=True, blank=True)
    comentario = models.TextField(blank=True)
    class Meta:
        db_table = 'Ceiba_votacion'

class EnlacesEnlace(models.Model):
    id = models.IntegerField(primary_key=True)
    orden = models.IntegerField()
    tipo = models.CharField(max_length=15L)
    file1 = models.CharField(max_length=100L)
    name1 = models.CharField(max_length=50L)
    file2 = models.CharField(max_length=100L, blank=True)
    name2 = models.CharField(max_length=50L, blank=True)
    description = models.CharField(max_length=200L)
    class Meta:
        db_table = 'Enlaces_enlace'

class FaqCategoria(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=3L)
    class Meta:
        db_table = 'Faq_categoria'

class FaqFaq(models.Model):
    id = models.IntegerField(primary_key=True)
    pregunta = models.TextField()
    respuesta = models.TextField()
    categoria = models.ForeignKey(FaqCategoria)
    subcategoria = models.ForeignKey('FaqSubcategoria')
    class Meta:
        db_table = 'Faq_faq'

class FaqSubcategoria(models.Model):
    id = models.IntegerField(primary_key=True)
    padre = models.ForeignKey(FaqCategoria)
    nombre = models.CharField(max_length=40L)
    class Meta:
        db_table = 'Faq_subcategoria'

class GrupoinvestAreaconocimiento(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100L)
    codigo = models.CharField(max_length=72) 
    class Meta:
        db_table = 'GrupoInvest_areaconocimiento'

class GrupoinvestAreainvestigacionanep(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100L)
    class Meta:
        db_table = 'GrupoInvest_areainvestigacionanep'

class GrupoinvestAreasinvestigacion(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=60L)
    descripcion = models.TextField()
    class Meta:
        db_table = 'GrupoInvest_areasinvestigacion'

class GrupoinvestCategoriainvestigador(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=40L)
    descripcion = models.TextField()
    
    def __unicode__(self):
        return u"%s" %(self.nombre)
    
    class Meta:
        db_table = 'GrupoInvest_categoriainvestigador'

class GrupoinvestCentro(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100L)
    class Meta:
        db_table = 'GrupoInvest_centro'

class GrupoinvestCodigovalidacion(models.Model):
    id = models.IntegerField(primary_key=True)
    investigador = models.ForeignKey('GrupoinvestInvestigador', unique=True)
    codigo = models.CharField(max_length=12L)
    intentos = models.IntegerField()
    fecha = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    last_selection = models.CharField(max_length=16L, blank=True)
    observ_inv = models.TextField(blank=True)
    observ_gestor = models.TextField(blank=True)
    class Meta:
        db_table = 'GrupoInvest_codigovalidacion'

class GrupoinvestDepartamento(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=120L)
    descripcion = models.TextField()
    codigo = models.CharField(max_length=5L)
    class Meta:
        db_table = 'GrupoInvest_departamento'

class GrupoinvestGrupoinves(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.TextField()
    direccion = models.TextField()
    telefono = models.CharField(max_length=20L, blank=True)
    fax = models.CharField(max_length=20L, blank=True)
    email = models.CharField(max_length=75L, blank=True)
    web = models.CharField(max_length=100L, blank=True)
    departamento = models.ForeignKey(GrupoinvestDepartamento, null=True, blank=True)
    centro = models.ForeignKey(GrupoinvestCentro, null=True, blank=True)
    instituto = models.ForeignKey('GrupoinvestInstituto', null=True, blank=True)
    area = models.ForeignKey(GrupoinvestAreasinvestigacion, null=True, blank=True)
    subarea = models.ForeignKey('GrupoinvestSubareasinvestigacion', null=True, blank=True)
    area_anep = models.ForeignKey(GrupoinvestAreainvestigacionanep, null=True, blank=True, related_name="anep_to_anep_inves")
    area_anep2 = models.ForeignKey(GrupoinvestAreainvestigacionanep, null=True, blank=True, related_name="anep_to_anep2_inves")
    area_anep3 = models.ForeignKey(GrupoinvestAreainvestigacionanep, null=True, blank=True, related_name="anep_to_anep3_inves")
    tag = models.CharField(max_length=255L)
    coordinador = models.ForeignKey('GrupoinvestInvestigador', null=True, blank=True)
    acronimo = models.CharField(max_length=20L, blank=True)
    activo = models.IntegerField(null=True, blank=True)
    descripcion = models.TextField(blank=True)
    
    def __unicode__(self):
        return u"%s" %(self.grupo)
    
    class Meta:
        db_table = 'GrupoInvest_grupoinves'

class GrupoinvestInstituto(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100L)
    class Meta:
        db_table = 'GrupoInvest_instituto'

class GrupoinvestInvestcvn(models.Model):
    id = models.IntegerField(primary_key=True)
    investigador = models.ForeignKey('GrupoinvestInvestigador', unique=True)
    cvnfile = models.FileField(max_length=100L, db_column='cvnFile', upload_to=PDF_ROOT) # Field name made lowercase.
    fecha_up = models.DateField(null=True, blank=True)
    fecha_cvn = models.DateField(null=True, blank=True)
    xmlfile = models.FileField(max_length=100L, db_column='xmlFile', upload_to=XML_ROOT) # Field name made lowercase.

    def __unicode__(self):
        return u"'%s' CVN: '%s'" %(self.investigador, self.cvnfile)


    class Meta:
        db_table = 'GrupoInvest_investcvn'
        verbose_name_plural = 'CVN Investigadores'
        

class GrupoinvestInvestigador(models.Model):
    user = models.ForeignKey('AuthUser', unique=True)
    grupo_activo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True, related_name="Perteneciente")
    grupo_a = models.ForeignKey(GrupoinvestGrupoinves, null=True, db_column='grupo_A_id', blank=True, related_name="Perteneciente(A)") # Field name made lowercase.
    grupo_b = models.ForeignKey(GrupoinvestGrupoinves, null=True, db_column='grupo_B_id', blank=True, related_name="Perteneciente(B)") # Field name made lowercase.
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=60L)
    apellido1 = models.CharField(max_length=60L)
    apellido2 = models.CharField(max_length=60L)
    nif = models.CharField(max_length=10L)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=6L)
    email = models.CharField(max_length=60L)
    telefono = models.CharField(max_length=60L, blank=True)
    categoria = models.ForeignKey(GrupoinvestCategoriainvestigador)
    departamento = models.ForeignKey(GrupoinvestDepartamento, null=True, blank=True)
    centro = models.ForeignKey(GrupoinvestCentro, null=True, blank=True)
    instituto = models.ForeignKey(GrupoinvestInstituto, null=True, blank=True)
    dedicacion = models.CharField(max_length=8L)
    file = models.CharField(max_length=100L, blank=True)
    areaconocimiento = models.ForeignKey(GrupoinvestAreaconocimiento, null=True, db_column='areaConocimiento_id', blank=True) # Field name made lowercase.
    descripcion = models.TextField(blank=True)
    confirma_grupo_a = models.IntegerField(null=True, db_column='confirma_grupo_A', blank=True) # Field name made lowercase.
    confirma_grupo_b = models.IntegerField(null=True, db_column='confirma_grupo_B', blank=True) # Field name made lowercase.
    sexenios = models.IntegerField(null=True, blank=True)
    inicio_sexenio = models.DateField(null=True, blank=True)
    fin_sexenio = models.DateField(null=True, blank=True)
    area_anep = models.ForeignKey(GrupoinvestAreainvestigacionanep, null=True, blank=True, related_name="anep_to_anep")
    area_anep2 = models.ForeignKey(GrupoinvestAreainvestigacionanep, null=True, blank=True, related_name="anep_to_anep2")
    area_anep3 = models.ForeignKey(GrupoinvestAreainvestigacionanep, null=True, blank=True, related_name="anep_to_anep3")
    cas_username = models.CharField(max_length=100L, blank=True)
    cod_persona = models.CharField(max_length=5L)
    cese = models.DateField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_last_update = models.DateTimeField(null=True, blank=True)
    rrhh_id = models.IntegerField(unique=True, null=True, blank=True)
 
    def __unicode__(self):
        return u"%s %s %s %s" %(self.nombre, self.apellido1, self.apellido2, self.nif)

    class Meta:
        db_table = 'GrupoInvest_investigador'
        verbose_name_plural = 'Investigadores'


class GrupoinvestOtromiembro(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo_activo = models.ForeignKey(GrupoinvestGrupoinves)
    user = models.ForeignKey('AuthUser', unique=True)
    nif = models.IntegerField()
    nombre = models.CharField(max_length=30L)
    apellidos = models.CharField(max_length=60L)
    categoria = models.ForeignKey(GrupoinvestCategoriainvestigador)
    centro_adscricion = models.CharField(max_length=60L)
    class Meta:
        db_table = 'GrupoInvest_otromiembro'

class GrupoinvestRrhh(models.Model):
    id = models.IntegerField(primary_key=True)
    cod_persona = models.IntegerField()
    pas_sn = models.CharField(max_length=100L, blank=True)
    nif = models.CharField(max_length=100L, blank=True)
    id_tipo_documento = models.CharField(max_length=100L, blank=True)
    nombre = models.CharField(max_length=100L, blank=True)
    apellido1 = models.CharField(max_length=100L, blank=True)
    apellido2 = models.CharField(max_length=100L, blank=True)
    sexo = models.CharField(max_length=100L, blank=True)
    f_nacimiento = models.DateField(null=True, blank=True)
    cod_nacionalidad = models.IntegerField(null=True, blank=True)
    nacionalidad = models.CharField(max_length=100L, blank=True)
    cod_pais_nac = models.IntegerField(null=True, blank=True)
    pais_nac = models.CharField(max_length=100L, blank=True)
    cod_prov_nac = models.IntegerField(null=True, blank=True)
    prov_nac = models.CharField(max_length=100L, blank=True)
    cod_loc_nac = models.IntegerField(null=True, blank=True)
    localidad_nac = models.CharField(max_length=100L, blank=True)
    telefono = models.CharField(max_length=100L, blank=True)
    correo_electronico = models.CharField(max_length=100L, blank=True)
    cod_tipo_via = models.IntegerField(null=True, blank=True)
    via = models.CharField(max_length=100L, blank=True)
    des_direccion = models.CharField(max_length=100L, blank=True)
    cod_postal = models.CharField(max_length=100L, blank=True)
    cod_localidad = models.IntegerField(null=True, blank=True)
    localidad = models.CharField(max_length=100L, blank=True)
    cod_provincia = models.IntegerField(null=True, blank=True)
    prov = models.CharField(max_length=100L, blank=True)
    id_pais = models.IntegerField(null=True, blank=True)
    pais = models.CharField(max_length=100L, blank=True)
    f_desde = models.DateField(null=True, blank=True)
    f_hasta = models.DateTimeField(null=True, blank=True)
    cod_cce = models.IntegerField(null=True, blank=True)
    categoria = models.CharField(max_length=100L, blank=True)
    rol = models.CharField(max_length=100L, blank=True)
    cod_departamento = models.IntegerField(null=True, blank=True)
    departamento = models.CharField(max_length=100L, blank=True)
    cod_area = models.CharField(max_length=100L, blank=True)
    area = models.CharField(max_length=100L, blank=True)
    cod_dedicacion = models.IntegerField(null=True, blank=True)
    dedicacion = models.CharField(max_length=100L, blank=True)
    cod_unidad = models.IntegerField(null=True, blank=True)
    unidad = models.CharField(max_length=100L, blank=True)
    cod_subunidad = models.IntegerField(null=True, blank=True)
    subunidad = models.CharField(max_length=100L, blank=True)
    cod_area_esp = models.CharField(max_length=100L, blank=True)
    area_esp = models.CharField(max_length=100L, blank=True)
    cod_departamento_esp = models.IntegerField(null=True, blank=True)
    departamento_esp = models.CharField(max_length=100L, blank=True)
    cod_unidad_esp = models.IntegerField(null=True, blank=True)
    unidad_esp = models.CharField(max_length=100L, blank=True)
    cod_subunidad_esp = models.IntegerField(null=True, blank=True)
    subunidad_esp = models.CharField(max_length=100L, blank=True)
    f_modif_datos_per = models.DateTimeField(null=True, blank=True)
    f_modif_nif = models.DateTimeField(null=True, blank=True)
    f_modif_domicilio = models.DateTimeField(null=True, blank=True)
    f_modif_vig_emp_plaza = models.DateTimeField(null=True, blank=True)
    f_modif_emp_plaza = models.DateTimeField(null=True, blank=True)
    f_modif_plaza = models.DateTimeField(null=True, blank=True)
    f_modif_docente = models.DateTimeField(null=True, blank=True)
    f_modif_pas = models.DateTimeField(null=True, blank=True)
    f_modif_otro_personal = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'GrupoInvest_rrhh'

class GrupoinvestSubareasinvestigacion(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=60L)
    descripcion = models.TextField()
    areaid = models.ForeignKey(GrupoinvestAreasinvestigacion, db_column='areaId_id') # Field name made lowercase.
    class Meta:
        db_table = 'GrupoInvest_subareasinvestigacion'

class InventinvArticulo(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    otras_universidades = models.TextField(blank=True)
    titulo = models.TextField(blank=True)
    autores = models.TextField(blank=True)
    ambito = models.CharField(max_length=15L, blank=True)
    revista = models.CharField(max_length=150L, blank=True)
    volumen = models.IntegerField(null=True, blank=True)
    numero = models.CharField(max_length=10L, blank=True)
    paginainic = models.IntegerField(null=True, db_column='paginaInic', blank=True) # Field name made lowercase.
    paginafin = models.IntegerField(null=True, db_column='paginaFin', blank=True) # Field name made lowercase.
    anio = models.CharField(max_length=4L, blank=True)
    fecha = models.DateField(null=True, blank=True)
    editorial = models.CharField(max_length=150L, blank=True)
    issn = models.CharField(max_length=9L, blank=True)
    es_indexado = models.IntegerField()
    jcr = models.ForeignKey('InventinvJcr', null=True, blank=True)
    jcr_social = models.ForeignKey('InventinvJcrsocial', null=True, blank=True)
    otras_bd = models.CharField(max_length=150L, blank=True)
    area = models.CharField(max_length=150L, blank=True)
    indice_impacto = models.CharField(max_length=20L, blank=True)
    posicion_revista = models.CharField(max_length=150L, blank=True)
    class Meta:
        db_table = 'InventInv_articulo'

class InventinvArticuloSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    articulo = models.ForeignKey(InventinvArticulo)
    segai = models.ForeignKey('SegaiSegai')
    class Meta:
        db_table = 'InventInv_articulo_segai'

class InventinvCapitulo(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    otras_universidades = models.TextField(blank=True)
    titulo = models.TextField(blank=True)
    autores = models.TextField(blank=True)
    pagina_inic = models.IntegerField(null=True, blank=True)
    pagina_fin = models.IntegerField(null=True, blank=True)
    anio = models.CharField(max_length=4L, blank=True)
    fecha = models.DateField(null=True, blank=True)
    libro = models.CharField(max_length=80L, blank=True)
    editores = models.TextField(blank=True)
    editorial = models.CharField(max_length=30L, blank=True)
    lugar = models.CharField(max_length=30L, blank=True)
    isbn = models.CharField(max_length=20L, blank=True)
    class Meta:
        db_table = 'InventInv_capitulo'

class InventinvCapituloSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    capitulo = models.ForeignKey(InventinvCapitulo)
    segai = models.ForeignKey('SegaiSegai')
    class Meta:
        db_table = 'InventInv_capitulo_segai'

class InventinvCongreso(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    titulo = models.TextField(blank=True)
    autores = models.TextField(blank=True)
    tipo_participacion = models.CharField(max_length=20L, blank=True)
    congreso = models.CharField(max_length=300L, blank=True)
    publicacion = models.CharField(max_length=150L, blank=True)
    lugar = models.CharField(max_length=60L, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    ambito = models.CharField(max_length=20L, blank=True)
    class Meta:
        db_table = 'InventInv_congreso'

class InventinvCongresoSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    congreso = models.ForeignKey(InventinvCongreso)
    segai = models.ForeignKey('SegaiSegai')
    class Meta:
        db_table = 'InventInv_congreso_segai'

class InventinvConvenio(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    otras_universidades = models.TextField(blank=True)
    titulo = models.TextField(blank=True)
    tipo = models.CharField(max_length=80L, blank=True)
    entidad_financiadora = models.TextField(blank=True)
    entidades_particip = models.TextField(blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    investigador_responsable = models.TextField(blank=True)
    universidad = models.CharField(max_length=150L, blank=True)
    num_investigadores = models.IntegerField(null=True, blank=True)
    num_inv_anyo = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    cuantia = models.DecimalField(null=True, max_digits=21, decimal_places=2, blank=True)
    otros_investigadores = models.TextField(blank=True)
    class Meta:
        db_table = 'InventInv_convenio'

class InventinvConvenioSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    convenio = models.ForeignKey(InventinvConvenio)
    segai = models.ForeignKey('SegaiSegai')
    class Meta:
        db_table = 'InventInv_convenio_segai'

class InventinvCreacionartistica(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    descripcion = models.TextField(blank=True)
    autores = models.TextField(blank=True)
    catalogo = models.IntegerField()
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    lugar = models.CharField(max_length=60L, blank=True)
    class Meta:
        db_table = 'InventInv_creacionartistica'

class InventinvCreacionartisticaSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    creacionartistica = models.ForeignKey(InventinvCreacionartistica)
    segai = models.ForeignKey('SegaiSegai')
    class Meta:
        db_table = 'InventInv_creacionartistica_segai'

class InventinvCvNotification(models.Model):
    id = models.IntegerField(primary_key=True)
    propietario = models.ForeignKey(GrupoinvestInvestigador)
    destinatario = models.ForeignKey(GrupoinvestInvestigador, related_name="to")
    fecha = models.DateTimeField()
    tipo = models.CharField(max_length=4L)
    estado = models.CharField(max_length=3L)
    updated = models.DateField(null=True, blank=True)
    item_cvndesc = models.CharField(max_length=40L, db_column='item_CVNdesc') # Field name made lowercase.
    item_cvntipo = models.IntegerField(db_column='item_CVNtipo') # Field name made lowercase.
    item_id = models.IntegerField()
    oper = models.IntegerField(null=True, blank=True)
    result = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'InventInv_cv_notification'

class InventinvCvPermiso(models.Model):
    id = models.IntegerField(primary_key=True)
    invest = models.ForeignKey(GrupoinvestInvestigador)
    dias_ins = models.IntegerField()
    dias_del = models.IntegerField()
    dias_edit = models.IntegerField()
    dias_pdte = models.IntegerField()
    fecha_ins = models.DateField(null=True, blank=True)
    fecha_del = models.DateField(null=True, blank=True)
    fecha_edit = models.DateField(null=True, blank=True)
    fecha_pdte = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'InventInv_cv_permiso'

class InventinvCvPermisoAuthDel(models.Model):
    id = models.IntegerField(primary_key=True)
    cv_permiso = models.ForeignKey(InventinvCvPermiso)
    investigador = models.ForeignKey(GrupoinvestInvestigador)
    class Meta:
        db_table = 'InventInv_cv_permiso_auth_del'

class InventinvCvPermisoAuthIns(models.Model):
    id = models.IntegerField(primary_key=True)
    cv_permiso = models.ForeignKey(InventinvCvPermiso)
    investigador = models.ForeignKey(GrupoinvestInvestigador)
    class Meta:
        db_table = 'InventInv_cv_permiso_auth_ins'

class InventinvCvnInfomodel(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(GrupoinvestInvestigador)
    tabla_id = models.IntegerField()
    fila_id = models.IntegerField()
    separador = models.IntegerField()
    date_added = models.DateTimeField()
    info = models.CharField(max_length=240L, blank=True)
    class Meta:
        db_table = 'InventInv_cvn_infomodel'

class InventinvEstancia(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    investigador = models.ForeignKey(GrupoinvestInvestigador, null=True, blank=True, related_name="estancia investigador")
    centro = models.CharField(max_length=150L, blank=True)
    localidad = models.CharField(max_length=150L, blank=True)
    pais = models.CharField(max_length=80L, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    duracion = models.IntegerField(null=True, blank=True)
    autores = models.TextField(blank=True)
    class Meta:
        db_table = 'InventInv_estancia'

class InventinvEvento(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    otras_universidades = models.TextField(blank=True)
    titulo = models.TextField(blank=True)
    tipo = models.TextField(blank=True)
    ambito = models.CharField(max_length=2L, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    organizador = models.TextField(blank=True)
    class Meta:
        db_table = 'InventInv_evento'

class InventinvJcr(models.Model):
    id = models.IntegerField(primary_key=True)
    jcr = models.CharField(max_length=3L)
    descripcion = models.CharField(max_length=100L)
    class Meta:
        db_table = 'InventInv_jcr'

class InventinvJcrsocial(models.Model):
    id = models.IntegerField(primary_key=True)
    jcr = models.CharField(max_length=100L)
    class Meta:
        db_table = 'InventInv_jcrsocial'

class InventinvLibro(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    otras_universidades = models.TextField(blank=True)
    titulo = models.TextField(blank=True)
    autores = models.TextField(blank=True)
    anio = models.CharField(max_length=4L, blank=True)
    fecha = models.DateField(null=True, blank=True)
    editor = models.CharField(max_length=30L, blank=True)
    lugar = models.CharField(max_length=30L, blank=True)
    isbn = models.CharField(max_length=20L, blank=True)
    class Meta:
        db_table = 'InventInv_libro'

class InventinvLibroSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    libro = models.ForeignKey(InventinvLibro)
    segai = models.ForeignKey('SegaiSegai')
    class Meta:
        db_table = 'InventInv_libro_segai'

class InventinvOfertacientifica(models.Model):
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    trabajo = models.TextField(blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'InventInv_ofertacientifica'

class InventinvOfertatecnica(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    tecnica = models.TextField(blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'InventInv_ofertatecnica'

class InventinvOtraactividad(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    descripcion = models.TextField(blank=True)
    autores = models.TextField(blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'InventInv_otraactividad'

class InventinvOtraactividadSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    otraactividad = models.ForeignKey(InventinvOtraactividad)
    segai = models.ForeignKey('SegaiSegai')
    class Meta:
        db_table = 'InventInv_otraactividad_segai'

class InventinvPatente(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    titulo = models.TextField(blank=True)
    inventores = models.TextField(blank=True)
    num_solicitud = models.CharField(max_length=20L, blank=True)
    pais = models.CharField(max_length=40L, blank=True)
    fecha = models.DateField(null=True, blank=True)
    entidad = models.TextField(blank=True)
    paises_extendido = models.TextField(blank=True)
    empresas = models.TextField(blank=True)
    class Meta:
        db_table = 'InventInv_patente'

class InventinvPatenteSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    patente = models.ForeignKey(InventinvPatente)
    segai = models.ForeignKey('SegaiSegai')
    class Meta:
        db_table = 'InventInv_patente_segai'

class InventinvTesis(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    otras_universidades = models.TextField(blank=True)
    doctorando = models.CharField(max_length=300L, blank=True)
    titulo = models.TextField(blank=True)
    universidad = models.CharField(max_length=150L, blank=True)
    facultad = models.CharField(max_length=150L, blank=True)
    fecha = models.DateField(null=True, blank=True)
    directores = models.TextField(blank=True)
    calificacion = models.CharField(max_length=25L, blank=True)
    class Meta:
        db_table = 'InventInv_tesis'

class InventinvTesisSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    tesis = models.ForeignKey(InventinvTesis)
    segai = models.ForeignKey('SegaiSegai')
    class Meta:
        db_table = 'InventInv_tesis_segai'

class InventinvTesisaprobada(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey(GrupoinvestGrupoinves, null=True, blank=True)
    date_added = models.DateTimeField()
    anyadido_por = models.ForeignKey(GrupoinvestInvestigador)
    is_ull = models.IntegerField()
    otras_universidades = models.TextField(blank=True)
    doctorando = models.CharField(max_length=300L, blank=True)
    titulo = models.TextField(blank=True)
    universidad = models.CharField(max_length=150L, blank=True)
    facultad = models.CharField(max_length=150L, blank=True)
    fecha = models.DateField(null=True, blank=True)
    directores = models.TextField(blank=True)
    class Meta:
        db_table = 'InventInv_tesisaprobada'

class InventinvTesisaprobadaSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    tesisaprobada = models.ForeignKey(InventinvTesisaprobada)
    segai = models.ForeignKey('SegaiSegai')
    class Meta:
        db_table = 'InventInv_tesisaprobada_segai'

class OapiOficina(models.Model):
    id = models.IntegerField(primary_key=True)
    campus = models.CharField(max_length=30L)
    edificio = models.CharField(max_length=30L)
    direccion = models.TextField()
    class Meta:
        db_table = 'Oapi_oficina'

class OapiPersonal(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30L)
    apellido1 = models.CharField(max_length=30L)
    apellido2 = models.CharField(max_length=30L)
    nif = models.CharField(max_length=10L)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=6L)
    email = models.CharField(max_length=60L)
    telefono = models.CharField(max_length=60L, blank=True)
    movil = models.CharField(max_length=60L, blank=True)
    oficina = models.ForeignKey(OapiOficina, null=True, blank=True)
    class Meta:
        db_table = 'Oapi_personal'

class ProyinvestEntidadfinanciadora(models.Model):
    id = models.IntegerField(primary_key=True)
    entidad = models.CharField(max_length=80L)
    class Meta:
        db_table = 'ProyInvest_entidadfinanciadora'

class ProyinvestMensajemantenimiento(models.Model):
    id = models.IntegerField(primary_key=True)
    activo = models.IntegerField()
    texto = models.TextField()
    mantenimiento = models.IntegerField()
    actualizacion = models.IntegerField()
    aviso = models.IntegerField()
    fecha = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'ProyInvest_mensajemantenimiento'

class ProyinvestProyectoinvestigacion(models.Model):
    id = models.IntegerField(primary_key=True)
    is_ull = models.IntegerField()
    titulo = models.TextField(blank=True)
    investigador_externo = models.IntegerField()
    nombre_inv_externo = models.CharField(max_length=150L, blank=True)
    email_inv_externo = models.CharField(max_length=150L, blank=True)
    referencia = models.CharField(max_length=30L, blank=True)
    organismo = models.TextField(blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    cuantia = models.DecimalField(null=True, max_digits=21, decimal_places=2, blank=True)
    num_inv = models.IntegerField(null=True, blank=True)
    num_inv_anyo = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    date_added = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'ProyInvest_proyectoinvestigacion'

class ProyinvestProyectoinvestigacionEntidadFinanciadora(models.Model):
    id = models.IntegerField(primary_key=True)
    proyectoinvestigacion = models.ForeignKey(ProyinvestProyectoinvestigacion)
    entidadfinanciadora = models.ForeignKey(ProyinvestEntidadfinanciadora)
    class Meta:
        db_table = 'ProyInvest_proyectoinvestigacion_entidad_financiadora'

class ProyinvestProyectoinvestigacionInvestigadorPrincipal(models.Model):
    id = models.IntegerField(primary_key=True)
    proyectoinvestigacion = models.ForeignKey(ProyinvestProyectoinvestigacion)
    investigador = models.ForeignKey(GrupoinvestInvestigador)
    class Meta:
        db_table = 'ProyInvest_proyectoinvestigacion_investigador_principal'

class ProyinvestProyectoinvestigacionOtrosInvestigadores(models.Model):
    id = models.IntegerField(primary_key=True)
    proyectoinvestigacion = models.ForeignKey(ProyinvestProyectoinvestigacion)
    investigador = models.ForeignKey(GrupoinvestInvestigador)
    class Meta:
        db_table = 'ProyInvest_proyectoinvestigacion_otros_investigadores'

class ProyinvestProyectoinvestigacionSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    proyectoinvestigacion = models.ForeignKey(ProyinvestProyectoinvestigacion)
    segai = models.ForeignKey('SegaiSegai')
    class Meta:
        db_table = 'ProyInvest_proyectoinvestigacion_segai'

class ProyinvestProyectosigidi(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=30L)
    titulo = models.CharField(max_length=400L)
    descripcion = models.CharField(max_length=400L)
    class Meta:
        db_table = 'ProyInvest_proyectosigidi'

class SegaiSegai(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=150L)
    borrado = models.IntegerField()
    class Meta:
        db_table = 'Segai_segai'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80L, unique=True)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthMessage(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('AuthUser')
    message = models.TextField()
    class Meta:
        db_table = 'auth_message'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100L)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30L)#, unique=True)
    first_name = models.CharField(max_length=30L)
    last_name = models.CharField(max_length=30L)
    email = models.CharField(max_length=75L)
    password = models.CharField(max_length=128L)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()



    def __unicode__(self):
        return u"'%s' e-mail: '%s'" %(self.username, self.email)
    
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = 'auth_user_user_permissions'

class CaptchaCaptchastore(models.Model):
    id = models.IntegerField(primary_key=True)
    challenge = models.CharField(max_length=32L)
    response = models.CharField(max_length=32L)
    hashkey = models.CharField(max_length=40L, unique=True)
    expiration = models.DateTimeField()
    class Meta:
        db_table = 'captcha_captchastore'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200L)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100L)
    app_label = models.CharField(max_length=100L)
    model = models.CharField(max_length=100L)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40L, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100L)
    name = models.CharField(max_length=50L)
    class Meta:
        db_table = 'django_site'

class TaggingTag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L, unique=True)
    class Meta:
        db_table = 'tagging_tag'

class TaggingTaggeditem(models.Model):
    id = models.IntegerField(primary_key=True)
    tag = models.ForeignKey(TaggingTag)
    content_type = models.ForeignKey(DjangoContentType)
    object_id = models.IntegerField()
    class Meta:
        db_table = 'tagging_taggeditem'

