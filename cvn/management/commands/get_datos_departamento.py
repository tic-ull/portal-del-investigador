# -*- encoding: utf8 -*-
from django.db.models import Q
import datetime
from viinvDB.models import GrupoinvestInvestigador, GrupoinvestDepartamento
from cvn.models import Usuario, Publicacion, Congreso, Proyecto, Convenio, TesisDoctoral

def none_to_zero(element):
    return element if not element is None else 0

def date_add(date, years, months, days):
    years = none_to_zero(years)
    months = none_to_zero(months)
    days = none_to_zero(days)
    return datetime.date(date.years + years, date.months + months, date.days + days)

class Get_datos_departamento:

    def __init__(self, identificador, year, tipo="departamento"):
        # Comprobar que los parametros son correctos
        assert(year.isdigit())
        assert (tipo == "departamento" or tipo == "instituto")
        assert(identificador.isdigit())
        
        # Almacenar las fechas para las consultas
        self.year = int(year)
        self.fecha_inicio_max = datetime.date(self.year, 12, 31)
        self.fecha_fin_min = datetime.date(self.year, 1, 1) 
        
        ''' Consulta a la base de datos los investigadores.
        self.tabla_investigadores => tabla con datos de los investigadores para ser usada fuera de la librería
        self.investigadores => dni de los investigadores para usar en otras consultas. Son necesarios los dni ya que
        estas consultas se pueden hacer en otra bbdd.'''
        self.tabla_investigadores, self.investigadores = self.query_investigadores(int(identificador), tipo)

    def query_investigadores(self, identificador, tipo):
        investigadores = None
        if tipo == "departamento":
            investigadores = GrupoinvestInvestigador.objects.filter(departamento__id=identificador)
        else:
            investigadores = GrupoinvestInvestigador.objects.filter(instituto__id=identificador)
        
        investigadores = investigadores.filter(Q(fecha_inicio__isnull=False)&Q(fecha_inicio__lte=self.fecha_inicio_max))
        investigadores = investigadores.filter(Q(cese__isnull=True)|Q(cese__gte=self.fecha_fin_min))
        investigadores = investigadores.order_by('apellido1', 'apellido2')
        
        tabla_investigadores = []
        for i in investigadores:
            tabla_investigadores.append([i.nombre, i.apellido1, i.apellido2, i.categoria.nombre])

        lista_dni = [investigador.nif for investigador in investigadores]
        # Guardamos los objectos Usuario, de los investigadores GrupoinvestInvestigador
        # Se extraen de esta manera por estar en bbdd diferentes
        lista_investigadores = Usuario.objects.filter(documento__in=lista_dni)
        return tabla_investigadores, lista_investigadores

    def get_investigadores(self):
        return self.tabla_investigadores

    def get_libros(self):
        libros = Publicacion.objects.filter(
            Q(usuario__in=self.investigadores) &
            Q(fecha__year=self.year) &
            Q(tipo_de_produccion='Libro')
        ).order_by('fecha')
        return list(libros)
    
    def get_capitulos(self): 
        capitulos = Publicacion.objects.filter(
            Q(usuario__in=self.investigadores) &
            Q(fecha__year=self.year) &
            Q(tipo_de_produccion='Capítulo de Libro')
        ).order_by('fecha')
        return list(capitulos)

    def get_articulos(self): 
        publicaciones = Publicacion.objects.filter(
            Q(usuario__in=self.investigadores) &
            Q(fecha__year=self.year) &
            Q(tipo_de_produccion='Artículo')
        ).order_by('fecha')
        return list(publicaciones)

    def get_congresos(self):
        congresos = Congreso.objects.filter(
            Q(usuario__in=self.investigadores)&
            Q(fecha_realizacion__year=self.year)
        ).order_by('fecha_realizacion')
        return list(congresos)

    def get_proyectos(self):
        proyectos = Proyecto.objects.filter(
            Q(usuario__in=self.investigadores)&
            Q(fecha_inicio__isnull=False)&
            Q(fecha_de_inicio__lte=self.fecha_inicio_max)
        ).order_by('fecha_de_inicio')
        
        proyectos_list = []
        for proyecto in proyectos:
            if proyecto.fecha_de_fin: # Si el proyecto usa fecha_de_fin en lugar de duracion
                if proyecto.fecha_de_fin >= self.fecha_fin_min:
                    proyectos_list.append(proyecto)
            else: # Si el proyecto usa duracion_anyos, ...meses ...dias    
                fecha_db_fin = date_add(proyecto.fecha_de_inicio,
                                        proyecto.duracion_anyos,
                                        proyecto.duracion_meses,
                                        proyecto.duracion_dias)
                if fecha_db_fin >= self.fecha_fin_min:
                    convenios_list.append(convenio) 
        return proyectos_list

    def get_convenios(self):
        convenios = Convenio.objects.filter(
            Q(usuario__in=self.investigadores)&
            Q(fecha_de_inicio__isnull=False)&
            Q(fecha_de_inicio__lte=self.fecha_inicio_max)
        ).order_by('fecha_de_inicio') 

        convenios_list = []
        for convenio in convenios:
            fecha_db_fin = date_add(convenio.fecha_de_inicio,
                                    convenio.duracion_anyos,
                                    convenio_duracion_meses,
                                    convenio_duracion_dias)
            if fecha_db_fin >= self.fecha_fin_min:
                convenios_list.append(convenio)
        return convenios_list

    def get_tesis(self):
        tesis = TesisDoctoral.objects.filter(
            Q(usuario__in=self.investigadores)&
            Q(fecha_de_lectura__year=self.year)
        ).order_by('fecha_de_lectura')
        return list(tesis)
