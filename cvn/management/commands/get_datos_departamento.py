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
        assert(year.isdigit())
        assert (tipo == "departamento" or tipo == "instituto")
        assert(identificador.isdigit())
        self.identificador = int(identificador)
        self.year = int(year)
        self.tipo = tipo
        self.table = self.setTable()
        # Fechas minima y maxima por las que se considera que una persona, proyecto, etc. pertenecen a un año.
        self.fecha_inicio_max = datetime.date(self.year, 12, 31)
        self.fecha_fin_min = datetime.date(self.year, 1, 1)
        self.set_investigadores()

    def setTable(self):
        if self.tipo == "departamento":
            return GrupoinvestDepartamento
        else:
            return GrupoinvestInstituto

    # Retorna los investigadores que pertenezcan al departamento/instituto
    def get_investigadores(self):
        return self.tabla_investigadores

    def set_investigadores(self):
        # Lista con objetos GrupoinvestInvestigador
        investigadores = None
        if self.tipo == "departamento":
            investigadores = GrupoinvestInvestigador.objects.filter(departamento__id=self.identificador)
        else:
            investigadores = GrupoinvestInvestigador.objects.filter(instituto__id=self.identificador)
        # Filter the users that where active on the selected year
        investigadores = investigadores.filter(Q(fecha_inicio__isnull=False)&Q(fecha_inicio__lte=self.fecha_inicio_max))
        investigadores = investigadores.filter(Q(cese__isnull=True)|Q(cese__gte=self.fecha_fin_min))
        investigadores = investigadores.order_by('apellido1', 'apellido2')
        investigadores = list(investigadores)
        # Lista con informacion de investigadores
        self.tabla_investigadores = []
        for i in investigadores:
            self.tabla_investigadores.append([i.nombre, i.apellido1, i.apellido2, i.categoria.nombre])

        lista_dni = [investigador.nif for investigador in investigadores]
        # Guardamos los objectos Usuario, de los investigadores GrupoinvestInvestigador
        # Se extraen de esta manera por estar en bbdd diferentes
        self.investigadores = Usuario.objects.filter(documento__in=lista_dni)

    def get_libros(self):
        return list(Publicacion.objects.filter(Q(usuario__in=self.investigadores) & Q(fecha__year=self.year) & Q(tipo_de_produccion='Libro')))
    
    def get_capitulos(self): 
        return list(Publicacion.objects.filter(Q(usuario__in=self.investigadores) & Q(fecha__year=self.year) & Q(tipo_de_produccion='Capítulo de Libro')))

    def get_articulos(self): 
        return list(Publicacion.objects.filter(Q(usuario__in=self.investigadores) & Q(fecha__year=self.year) & Q(tipo_de_produccion='Artículo')))

    def get_congresos(self):
        return list(Congreso.objects.filter(Q(usuario__in=self.investigadores)&Q(fecha_realizacion__year=self.year)))

    def get_proyectos(self):
        proyectos = Proyecto.objects.filter(Q(usuario__in=self.investigadores)&Q(fecha_inicio__isnull=False)&Q(fecha_de_inicio__lte=self.fecha_inicio_max))
        proyectos_list = []
        for proyecto in proyectos:
            if proyecto.fecha_de_fin: # Si el proyecto usa fecha_de_fin en lugar de duracion
                if proyecto.fecha_de_fin > self.fecha_fin_min:
                    proyectos_list.append(proyecto)
            else: # Si el proyecto usa duracion_anyos, ...meses ...dias    
                fecha_db_fin = date_add(proyecto.fecha_de_inicio,\
                                        proyecto.duracion_anyos,\
                                        proyecto.duracion_meses,\
                                        proyecto.duracion_dias)
                if fecha_db_fin > self.fecha_fin_min:
                    convenios_list.append(convenio)
                
        return proyectos_list

    def get_convenios(self):
        convenios = Convenio.objects.filter(Q(usuario__in=self.investigadores)&Q(fecha_de_inicio__isnull=False)&Q(fecha_de_inicio__lte=self.fecha_inicio_max)) 
        convenios_list = []
        for convenio in convenios:
            fecha_db_fin = date_add(convenio.fecha_de_inicio,\
                                    convenio.duracion_anyos,\
                                    convenio_duracion_meses,\
                                    convenio_duracion_dias)
            if fecha_db_fin > self.fecha_fin_min:
                convenios_list.append(convenio)
        return convenios_list

    def get_tesis(self):
        return list(TesisDoctoral.objects.filter(Q(usuario__in=self.investigadores)&Q(fecha_de_lectura__year=self.year)))
