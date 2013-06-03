# -*- encoding: utf-8 -*-
from django.db import models
# Importar modelos de la aplicación vieja de Viinv
from viinvDB.models import GrupoinvestInvestigador

# Modelo para almacenar los datos del investigador del Fecyt
class Usuario(models.Model):
	"""
	Datos personales del usuario
	
	https://cvn.fecyt.es/editor/cvn.html?locale=spa#IDENTIFICACION
	"""	
	investigador        = models.OneToOneField(GrupoinvestInvestigador, blank=True, null=True)
 	# Campos recomendados	
	primer_apellido     = models.CharField(u'Primer Apellido', max_length=50, blank=True, null=True)
	segundo_apellido    = models.CharField(u'Segundo Apellido', max_length=50, blank=True, null=True)
	nombre              = models.CharField(u'Nombre', max_length=50, blank=True, null=True)
	sexo                = models.CharField(u'Sexo', max_length=10, blank=True, null=True)
	fecha_nacimiento    = models.DateField(u'Fecha de nacimiento', blank=True, null=True)
	tipo_documento      = models.CharField(u'Tipo de Documento', max_length=20, blank=True, null=True)
	correo_electronico  = models.EmailField(u'Correo electrónico', blank=True, null=True)	
	documento           = models.CharField(u'Documento', max_length=20, blank=True, null=True)
	
	# NOTE Debería existir una tabla teléfono
	telefono_fijo_cod   = models.CharField(u'Código internacional', max_length=16, blank=True, null=True)
	telefono_fijo_num   = models.CharField(u'Número', max_length=32, blank=True, null=True) 
	telefono_fijo_ext   = models.CharField(u'Extensión', max_length=16, blank=True, null=True)
	
	telefono_fax_cod    = models.CharField(u'Código internacional', max_length=16, blank=True, null=True)
	telefono_fax_num    = models.CharField(u'Número', max_length=32, blank=True, null=True) 
	telefono_fax_ext    = models.CharField(u'Extensión', max_length=16, blank=True, null=True)
	
	telefono_movil_cod  = models.CharField(u'Código internacional', max_length=16, blank=True, null=True)
	telefono_movil_num  = models.CharField(u'Número', max_length=32, blank=True, null=True) 
	telefono_movil_ext  = models.CharField(u'Extensión', max_length=16, blank=True, null=True)
	
	# Más campos
	imagen              = models.ImageField(upload_to = 'static/files', blank=True, null=True) #TODO ruta a directorio de imagenes
	pagina_web_personal = models.URLField(u'Web personal', max_length=128, blank=True, null=True)

	direccion            = models.CharField(u'Dirección de contacto', max_length=300, blank=True, null=True)
	resto_direccion      = models.CharField(u'Resto de dirección de contacto', max_length=300, blank=True, null=True)
	codigo_postal        = models.CharField(u'Código postal', max_length=16, blank=True, null=True)
	
 	ciudad_de_contacto   = models.CharField(u'Ciudad de contacto', max_length=64, blank=True, null=True)
	pais_de_contacto     = models.CharField(u'País de contacto', max_length=64, blank=True, null=True)
	comunidad            = models.CharField(u'Comunidad autónoma/Región de contacto', max_length=64, blank=True, null=True)

	provincia            = models.CharField(u'Provincia', max_length=64, blank=True, null=True)
	nacionalidad		 = models.CharField(u'Nacionalidad', max_length=64, blank=True, null=True) 

 	ciudad_de_nacimiento = models.CharField(u'Ciudad de nacimiento', max_length=64, blank=True, null=True)
	pais_de_nacimiento   = models.CharField(u'País de nacimiento', max_length=64, blank=True, null=True)
	comunidad_nacimiento = models.CharField(u'Comunidad autónoma/Región de nacimiento', max_length=64, blank=True, null=True)
 
	created_at = models.DateTimeField(u'Creado', auto_now_add = True)
	updated_at = models.DateTimeField(u'Actualizado', auto_now = True)

	def __unicode__(self):
		return u"%s %s %s  con documento %s" %(self.nombre, self.primer_apellido, self.segundo_apellido, self.documento)



class SituacionProfesional(models.Model):
	"""
	Situación profesional actual y anterior. Se fusionan ambas tablas del editor del Fecyt en una.
	Para saber cuando es la situación profesional actual, basta con mirar si el registro tiene
	algún valor en el campo fecha de fin. 
	
	http://cvn.fecyt.es/editor/cvn.html?locale=spa#SITUACION_PROFESIONAL
	"""
	usuario = models.ForeignKey(Usuario) # Relación 1:N 
	
	# Campos recomendados 
	nombre_de_la_entidad = models.CharField(u'Nombre de la entidad', max_length=128, blank=True, null=True)
	tipo_de_entidad = models.CharField(u'Tipo de entidad', max_length=32, blank=True, null=True)
	categoria_or_puesto = models.CharField(u'Categoría/puesto o cargo', max_length=32, blank=True, null=True)
	fecha_de_inicio = models.DateField(u'Fecha de inicio', blank=True, null=True)
	
	modalidad_del_contrato = models.CharField(u'Modalidad del contrato', max_length=32, blank=True, null=True)
	
	# NOTE Tabla Cargo o actividades anteriores
	fecha_de_fin = models.DateField(u'Fecha de finalización', blank = True, null = True)
	duracion_anyos = models.IntegerField(u'Duración en años', blank=True, null=True)
	duracion_meses = models.IntegerField(u'Duración en meses', blank=True, null=True)
	duracion_dias = models.IntegerField(u'Duración en días', blank=True, null=True)
	#

	especializacion_primaria = models.CharField(u'Especialización primaria (Código Unesco)', max_length=64, blank=True, null=True)
	especializacion_secundaria = models.CharField(u'Especialización secundaria (Código Unesco)', max_length=64, blank=True, null=True) 
	especializacion_terciaria = models.CharField(u'Especialización terciaria (Código Unesco)', max_length=64, blank=True, null=True)

	
	# NOTE Si no tiene fecha de finalización es la dedicación actual
	dedicacion_profesional = models.TextField(u'Dedicación Profesional', blank = True, null = True)

	tipo_de_dedicacion = models.CharField(u'Tipo de dedicación', max_length=16, blank = True, null = True)
	palabras_clave_dedicacion = models.CharField(u'Palabras clave dedicación', max_length=64, blank = True, null = True)

    # Más campos
	docente = models.CharField(u'Docente', max_length=4, blank = True, null = True)
	tipo_de_actividad_de_gestion = models.CharField(u'Tipo de actividad de gestión', max_length=64, blank = True, null = True)
	
	# NOTE Tabla Cargo o actividades anteriores
	facultad_or_escuela = models.CharField(u'Facultad, escuela, etc.', max_length=64, blank=True, null=True)
	departamento_or_servicio = models.CharField(u'Departamento o servicio', max_length=64, blank=True, null=True) 
	
	
	ciudad_de_trabajo = models.CharField(u'Ciudad de Trabajo', max_length=64, blank=True, null=True)
	pais_de_trabajo = models.CharField(u'País de trabajo', max_length=32, blank=True, null=True)
	comunidad_or_region_trabajo = models.CharField(u'Comunidad autónoma/Región de trabajo', max_length=64, blank=True, null=True)

	telefono_fijo_cod   = models.CharField(u'Código internacional', max_length=12, blank=True, null=True)
	telefono_fijo_num   = models.PositiveIntegerField(u'Número', blank=True, null=True) 
	telefono_fijo_ext   = models.PositiveIntegerField(u'Extensión', blank=True, null=True)
	
	telefono_fax_cod    = models.CharField(u'Código internacional', max_length=12, blank=True, null=True)
	telefono_fax_num    = models.PositiveIntegerField(u'Número', blank=True, null=True) 
	telefono_fax_ext    = models.PositiveIntegerField(u'Extensión', blank=True, null=True)
	
	# NOTE se permiten múltiples correos => Tabla	
	correo_electronico = models.EmailField(u'Correo electrónico', blank=True, null=True) 

	interes_doc_investigacion = models.TextField(u'Interés para docencia y/o investigación', blank=True, null=True)
		
	created_at       = models.DateTimeField(u'Creado', auto_now_add = True)
	updated_at       = models.DateTimeField(u'Actualizado', auto_now = True)


	def __unicode__(self):
		return u"%s, %s en %s" %(self.usuario, self.categoria_or_puesto, self.nombre_de_la_entidad)
		
	class Meta:
		verbose_name_plural = u'Actividades profesionales'

########################################## Actividad científica y tecnológica ##########################################

# Clase Padre para los diferentes autores de las actividades científicas y tecnológicas
class Autor(models.Model):
	"""
		Autores en publicaciones, congresos, jornadas,...
	"""	
	firma            = models.CharField(u'Firma', max_length = 30, blank = True, null = True)
	nombre           = models.CharField(u'Nombre', max_length = 50, blank = True, null = True)
	primer_apellido  = models.CharField(u'Primer Apellido', max_length = 50, blank = True, null = True)
	segundo_apellido = models.CharField(u'Segundo Apellido', max_length = 50, blank = True, null = True)
	posicion         = models.CharField(u'Posición', max_length = 10, blank = True, null = True)


class Produccion(models.Model):
	"""
		Producción científica: Índice H.
		https://cvn.fecyt.es/editor/cvn.html?locale=spa#ACTIVIDAD_CIENTIFICA
	"""	
	usuario  = models.ForeignKey(Usuario)
	# Campos recomendados
	indice_h = models.CharField(u'Índice H', max_length = 100, blank = True, null = True) 
	fecha    = models.DateField(u'Fecha', blank = True, null = True)

	created_at = models.DateTimeField(u'Creado', auto_now_add = True)
	updated_at = models.DateTimeField(u'Actualizado', auto_now = True)

	
	def __unicode__(self):
		return u"%s [%s]" %(self.indice_h, self.usuario)

	class Meta:
		verbose_name_plural = u'Producciones científicas'
		
		
class Publicacion(models.Model):
	"""
		Publicaciones, documentos científicos y técnicos.
		https://cvn.fecyt.es/editor/cvn.html?locale=spa#ACTIVIDAD_CIENTIFICA
	"""	
	#usuario    = models.ForeignKey(Usuario)
	usuario    = models.ManyToManyField(Usuario) # Una publicación puede pertenecer a varios usuarios. 	
	created_by = models.ForeignKey(Usuario, related_name = u'Introducido')
	
	# Campos recomendados	
	tipo_de_produccion = models.CharField(u'Tipo de producción', max_length = 50, blank = True, null = True)
	fecha              = models.DateField(u'Fecha', blank = True, null = True)
	titulo_publicacion = models.CharField(u'Título de la publicación', max_length = 100, blank = True, null = True) 

	tipo_de_soporte    = models.CharField(u'Tipo de soporte', max_length = 100, blank = True, null = True) 
	nombre_publicacion = models.CharField(u'Nombre de la publicación', max_length = 100, blank = True, null = True)
	editorial          = models.CharField(u'Editorial', max_length = 100, blank = True, null = True)
	
	# Volumen 
	volumen        = models.CharField(u'Volumen', max_length = 50, blank = True, null = True)
	numero         = models.CharField(u'Número', max_length = 50, blank = True, null = True)
	pagina_inicial = models.IntegerField(u'Página Inicial', max_length = 50, blank = True, null = True)
	pagina_final   = models.IntegerField(u'Página Final', max_length = 50, blank = True, null = True)

	# Otros campos
	posicion_sobre_total = models.IntegerField(u'Posición sobre total', blank = True, null = True)
	en_calidad_de        = models.CharField(u'En calidad de', max_length = 100, blank = True, null = True) 
	
	isbn = models.CharField(u'ISBN', max_length = 50, blank = True, null = True)
	issn = models.CharField(u'ISSN', max_length = 50, blank = True, null = True)

	deposito_legal = models.CharField(u'Depósito legal', max_length = 50, blank = True, null = True)
	url            = models.URLField(u'URL', max_length = 128, blank = True, null = True)
	coleccion      = models.CharField(u'Colección', max_length = 50, blank = True, null = True)

	ciudad  = models.CharField(u'Ciudad de la titulación', max_length = 50,  blank = True, null = True)
	pais    = models.CharField(u'País de la titulación', max_length = 50, blank = True, null = True) 
	comunidad_or_region = models.CharField(u'Autónoma/Reg. de trabajo', max_length = 50, blank = True, null = True)

	# Índice de impacto	
	fuente_de_impacto    = models.CharField(u'Fuente de impacto', max_length = 20, blank = True, null = True)
	categoria            = models.CharField(u'Categoría', max_length = 20, blank = True, null = True)
	indice_de_impacto    = models.CharField(u'Índice de impacto', max_length = 20, blank = True, null = True)
	posicion             = models.IntegerField(u'Posicion', blank = True, null = True)
	num_revistas_catoria = models.IntegerField(u'Número de revistas en la categoría', blank = True, null = True)

	revista_25 = models.CharField(u'Revista dentro del 25%', max_length = 5, blank = True, null = True)
	
	# Citas	
	fuente_de_citas = models.CharField(u'Fuente de citas', max_length = 10, blank = True, null = True)
	citas           = models.CharField(u'Citas', max_length = 50, blank = True, null = True)

	publicacion_relevante = models.CharField(u'Publicación relevante', max_length = 5, blank = True, null = True)
	resenyas_en_revista   = models.CharField(u'Reseñas en revistas', max_length = 50, blank = True, null = True)

	# Traducciones
	# NOTE: Campo de autocompletado. Desde este control se permite seleccionar varias titulaciones de la norma.
	filtro = models.CharField(u'Filtro', max_length = 50, blank = True, null = True)
	resultados_destacados = models.TextField(u'Resultados destacados', blank = True, null = True)
	
	created_at = models.DateTimeField(u'Creado', auto_now_add = True)
	updated_at = models.DateTimeField(u'Actualizado', auto_now = True)

	
	def __unicode__(self):
		return "%s, %s" %(self.usuario, self.tipo_de_produccion)

	class Meta:
		verbose_name_plural = u'Publicaciones'


# Herencia de la tabla autor
class AutorPublicacion(Autor):
	"""
		Autores en publicaciones.
	"""
	publicacion = models.ForeignKey(Publicacion)

	def __unicode__(self):
		return u"%s %s" %(self.publicacion, self.nombre, self.primer_apellido)			
		
	class Meta:
		verbose_name_plural = u'Autores Publicaciones'
		
		
class Congreso(models.Model):
	"""
		Trabajos presentados en congresos nacionales o internacionales.
		# https://cvn.fecyt.es/editor/cvn.html?locale=spa#ACTIVIDAD_CIENTIFICA
	"""	
	usuario    = models.ForeignKey(Usuario)
	# Campos recomendados
	titulo             = models.CharField(u'Título', max_length = 100, blank = True, null = True) 
	fecha_realizacion  = models.DateField(u'Fecha de realización', blank = True, null = True)
	fecha_finalizacion = models.DateField(u'Fecha de finalización', blank = True, null = True)

	nombre_del_congreso   = models.CharField(u'Nombre del congreso', max_length = 100, blank = True, null = True)
	ciudad_de_realizacion = models.CharField(u'Ciudad de realización', max_length = 32, blank = True, null = True)
	pais_de_realizacion   = models.CharField(u'País de realización', max_length = 32, blank = True, null = True)
	comunidad_or_region_realizacion   = models.CharField(u'Comunidad autónoma/Región de realizacion', max_length = 32, blank = True, null = True)

	entidad_organizadora = models.CharField(u'Entidad organizadora', max_length = 100, blank = True, null = True) 
	ciudad               = models.CharField(u'Ciudad', max_length = 32, blank = True, null = True)
	pais                 = models.CharField(u'País', max_length = 32, blank = True, null = True)
	comunidad_or_region  = models.CharField(u'Comunidad autónoma/Región', max_length = 32, blank = True, null = True)

 	titulo_publicacion = models.CharField(u'Título de la publicación', max_length = 50, blank = True, null = True)

	# Más Campos
	tipo_evento             = models.CharField(u'Tipo evento', choices = (), max_length = 50, blank = True, null = True)
	tipo                    = models.CharField(u'Tipo', choices = (), max_length = 50, blank = True, null = True)
	fecha                   = models.DateField(u'Fecha', blank = True, null = True)
	nombre_de_publicacion   = models.CharField(u'Nombre de la publicación', max_length = 50, blank = True, null = True)
	comite_admision_externa = models.CharField(u'Con comité de admisión externa', choices = (), max_length = 50, blank = True, null = True)
	ambito_del_congreso     = models.CharField(u'Ámbito del congreso', choices = (), max_length = 30, blank = True, null = True)
	tipo_de_participacion   = models.CharField(u'Tipo de participación', choices = (), max_length = 40, blank = True, null = True)
	intervencion_por        = models.CharField(u'Intevención por', choices = (), max_length = 50, blank = True, null = True)
 	
	# Volumen 
	volumen        = models.CharField(u'Volumen', max_length = 50, blank = True, null = True)
	numero         = models.CharField(u'Número', max_length = 50, blank = True, null = True)
	pagina_inicial = models.IntegerField(u'Página Inicial', max_length = 50, blank = True, null = True)
	pagina_final   = models.IntegerField(u'Página Final', max_length = 50, blank = True, null = True)

	editorial = models.CharField(u'Editorial', max_length = 100, blank = True, null = True)

	isbn = models.CharField(u'ISBN', max_length = 50, blank = True, null = True)
	issn = models.CharField(u'ISSN', max_length = 50, blank = True, null = True)

	deposito_legal            = models.CharField(u'Depósito legal', max_length = 50, blank = True, null = True)
	publicacion_acta_congreso =	models.CharField(u'Publicación en acta congreso', max_length = 100, choices = (), blank = True, null = True)

	url = models.URLField(u'', max_length = 128, blank = True, null = True)

	pais = models.CharField(u'País', choices = (), max_length = 50, blank = True, null = True)
	comunidad_or_region = models.CharField(u'Comunidad Autónoma/Región', choices = (), max_length = 50, blank = True, null = True)

	created_at = models.DateTimeField(u'Creado', auto_now_add = True)
	updated_at = models.DateTimeField(u'Actualizado', auto_now = True)

	# TODO: unicode
	def __unicode__(self):
		return "%s, %s" %(self.usuario, self.tipo_de_produccion)
	
	class Meta:
		verbose_name_plural = u'Congresos'


# Herencia de la tabla autor
class AutorCongreso(Autor):
	"""
		Autores en congresos.
	"""
	congreso = models.ForeignKey(Congreso)

	def __unicode__(self):
		return u"%s %s" %(self.publicacion, self.nombre, self.primer_apellido)			
		
	class Meta:
		verbose_name_plural = u'Autores Congresos'
