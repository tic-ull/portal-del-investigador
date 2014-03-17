# -*- encoding: utf8 -*-
from django.db.models import Q
import datetime
from viinvDB.models import GrupoinvestInvestigador, GrupoinvestDepartamento
from cvn.models import Usuario, Publicacion, Congreso, Proyecto, Convenio, TesisDoctoral

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
        self.investigadores => objectos de investigadores para ser usada fuera de la librería
        self.usuarios => investigadores en el departamento activos en el año (estan en una bbdd diferentes que self.investigadores). Usado en el resto de consultas'''
        self.investigadores, self.usuarios = self.query_investigadores(int(identificador), tipo)

    def query_investigadores(self, identificador, tipo):
        investigadores = None
        if tipo == "departamento":
            investigadores = GrupoinvestInvestigador.objects.filter(departamento__id=identificador)
        else:
            investigadores = GrupoinvestInvestigador.objects.filter(instituto__id=identificador)
        
        investigadores = investigadores.filter(Q(fecha_inicio__isnull=False)&Q(fecha_inicio__lte=self.fecha_inicio_max))
        investigadores = investigadores.filter(Q(cese__isnull=True)|Q(cese__gte=self.fecha_fin_min))
        investigadores = investigadores.order_by('apellido1', 'apellido2')
        
        lista_dni = [investigador.nif for investigador in investigadores]
        # Guardamos los objectos Usuario, de los investigadores GrupoinvestInvestigador
        # Se extraen de esta manera por estar en bbdd diferentes
        usuarios = Usuario.objects.filter(documento__in=lista_dni)
        return investigadores, usuarios

    def get_investigadores(self):
        return self.investigadores

    def get_libros(self):
        libros = Publicacion.objects.filter(
            Q(usuario__in=self.usuarios) &
            Q(fecha__year=self.year) &
            Q(tipo_de_produccion='Libro')
        ).order_by('fecha')
        return list(libros)
    
    def get_capitulos(self): 
        capitulos = Publicacion.objects.filter(
            Q(usuario__in=self.usuarios) &
            Q(fecha__year=self.year) &
            Q(tipo_de_produccion='Capítulo de Libro')
        ).order_by('fecha')
        return list(capitulos)

    def get_articulos(self): 
        publicaciones = Publicacion.objects.filter(
            Q(usuario__in=self.usuarios) &
            Q(fecha__year=self.year) &
            Q(tipo_de_produccion='Artículo')
        ).order_by('fecha')
        return list(publicaciones)

    def get_congresos(self):
        congresos = Congreso.objects.filter(
            Q(usuario__in=self.usuarios)&
            Q(fecha_realizacion__year=self.year)
        ).order_by('fecha_realizacion')
        return list(congresos)

    def get_proyectos(self):
        proyectos = Proyecto.objects.filter(
            Q(usuario__in=self.usuarios)&
            Q(fecha_de_inicio__isnull=False)&
            Q(fecha_de_inicio__lte=self.fecha_inicio_max)
        ).order_by('fecha_de_inicio')
        
        proyectos_list = []
        for proyecto in proyectos:
            fecha_db_fin = proyecto.getFechaFin() 
            fecha_db_fin = fecha_db_fin if fecha_db_fin is not None else proyecto.fecha_de_inicio
            if fecha_db_fin >= self.fecha_fin_min:
                proyectos_list.append(proyecto) 
        return proyectos_list

    def get_convenios(self):
        convenios = Convenio.objects.filter(
            Q(usuario__in=self.usuarios)&
            Q(fecha_de_inicio__isnull=False)&
            Q(fecha_de_inicio__lte=self.fecha_inicio_max)
        ).order_by('fecha_de_inicio') 

        convenios_list = []
        for convenio in convenios:
            fecha_db_fin = convenio.getFechaFin()
            fecha_db_fin = fecha_db_fin if fecha_db_fin is not None else convenio.fecha_de_inicio
            if fecha_db_fin >= self.fecha_fin_min:
                convenios_list.append(convenio)
        return convenios_list

    def get_tesis(self):
        tesis = TesisDoctoral.objects.filter(
            Q(usuario__in=self.usuarios)&
            Q(fecha_de_lectura__year=self.year)
        ).order_by('fecha_de_lectura')
        return list(tesis)
