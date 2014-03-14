# -*- encoding: utf8 -*-
from django.db.models import Q
import datetime
from viinvDB.models import GrupoinvestInvestigador, GrupoinvestDepartamento
from cvn.models import Usuario, Publicacion, Congreso, Proyecto, Convenio, TesisDoctoral

class Get_datos_departamento:
    """
    Clase que consulta una BBDD a través de una conexión y obtiene
    todos los datos referentes a un departamento (instituto)
    Entrada:
        Conexión a la BBDD
        identificador del departamento o instituto
        tipo "departamento"|"instituto"
    Salida:
        datos_basicos: diccionario de datos
        investigadores: lista de tuplas con (nombre, primer apellido,
                                            segundo apellido, categoria)
        publicacion: diccionario: tipo de produccion (artículos, tesis,...)
         -> lista de tuplas
        actividad: diccionario: tipo de actividad (congresos, convenios...)
         -> lista de tuplas
    """
    TIPO_PRODUCCION = {'articulo': u'Artículo',
                  'libro': u'Libro',
                  'capitulo': u'Capítulo de Libro'}
    PRODUCCION = {u'Artículo': u'Artículos',
                  u'Libro': u'Libros',
                  u'Capítulo de Libro': u'Capítulos de libro'}
    def __init__(self, identificador, year, tipo="departamento"):
        #self.db_connection = db_connection
        assert(year.isdigit())
        assert (tipo == "departamento" or tipo == "instituto")
        assert(identificador.isdigit())
        self.identificador = int(identificador)
        self.year = int(year)
        self.tipo = tipo
        #self.setType()
        self.table = self.setTable()
        self.set_investigadores()

        self.datos_basicos = {}
        self.investigadores = []
        self.produccion = {}
        self.actividad = {}

    def setTable(self):
        if self.tipo == "departamento":
            return GrupoinvestDepartamento
        else:
            return GrupoinvestInstituto

    def get_datos_basicos(self):
        """
        Consulta para obtener los datos del departamento/instituto especificado
        """
        self.datos_basicos['nombre'] = self.table.objects.filter(id=self.identificador)[0]
        '''instruccion = """SELECT nombre
                         FROM {0}
                         WHERE id = {1}""".format(self.table,
                                                  self.identificador)
        cursor = self.db_connection.cursor()
        cursor.execute(instruccion)
        row = cursor.fetchone()
        self.datos_basicos['nombre'] = row[0]'''
        # TODO
        # get more data with the web service and fill the dictionary
        return self.datos_basicos

    '''def get_investigadores(self):
        self.query_data_investigadores()
        return tuple(self.investigadores)'''

    # Retorna los investigadores que pertenezcan al departamento/instituto
    def get_investigadores(self):
        return self.tabla_investigadores
    # nombre, apellido1, apellido2, nif, categoria
        '''instruccion = """SELECT DISTINCT nombre, apellido1, apellido2, nif
                         FROM {0}_GrupoInvest_investigador
                         WHERE {1} = {2}
                         ORDER BY apellido1""".format("mem12", self.tipo_id,
                                                      self.identificador)
        cursor = self.db_connection.cursor()
        cursor.execute(instruccion)
        rows = cursor.fetchall()
        # now adding the category and creating the list'''
        '''for investigador in rows:
            nif = investigador[3]
            instruccion = """SELECT nombre
                             FROM {0}_GrupoInvest_categoriainvestigador
                             WHERE id = (
                             SELECT categoria_id
                             FROM {0}_GrupoInvest_investigador
                             WHERE nif = "{1}")""".format("mem12", nif)

            cursor.execute(instruccion)
            row = cursor.fetchone()
            investigador = tuple(list(investigador[:-1]) + list(row))
            self.investigadores.append(investigador)'''

    def set_investigadores(self):
        # Lista con objetos GrupoinvestInvestigador
        investigadores = None
        if self.tipo == "departamento":
            investigadores = GrupoinvestInvestigador.objects.filter(departamento__id=self.identificador)
        else:
            investigadores = GrupoinvestInvestigador.objects.filter(instituto__id=self.identificador)
        # Filter the users that where active on the selected year
        fecha_inicio = datetime.date(self.year, 12, 31)
        fecha_fin = datetime.date(self.year, 1, 1)
        investigadores = investigadores.filter(Q(fecha_inicio__isnull=False)&Q(fecha_inicio__lte=fecha_inicio))
        investigadores = investigadores.filter(Q(cese__isnull=True)|Q(cese__gte=fecha_fin))
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

    # Actividad Científica
    '''def get_actividad(self):
        self.dataCongresos()
        self.dataProyectos()
        self.dataConvenios()
        self.dataTesis()
        return self.actividad'''

    def get_congresos(self):
        return list(Congreso.objects.filter(Q(usuario__in=self.investigadores)&Q(fecha_realizacion__year=self.year)))
        '''inst_congreso = """
                            SELECT DISTINCT congreso_id
                            FROM {0}_cvn_congreso_usuario
                            WHERE usuario_id IN (
                                {1})""".format("mem12", self.inst_base)
        instruccion = """
                         SELECT DISTINCT titulo, nombre_del_congreso, autores,\
                            ciudad_de_realizacion, fecha_realizacion
                         FROM {0}_cvn_congreso
                         WHERE YEAR(fecha_realizacion) = {1}
                         AND id IN (
                         {2})
                         ORDER BY fecha_realizacion""".format("mem12",
                                                              self.year,
                                                              inst_congreso)
        cursor = self.db_connection.cursor()
        cursor.execute(instruccion)
        congresos = cursor.fetchall()
        self.actividad["congresos"] = congresos'''

    def get_proyectos(self):
        return list(Proyecto.objects.filter(Q(usuario__in=self.investigadores)&Q(fecha_de_inicio__year=self.year)))
        '''inst_proyecto = """
                           SELECT DISTINCT proyecto_id
                           FROM {0}_cvn_proyecto_usuario
                           WHERE usuario_id IN (
                               {1})""".format("mem12", self.inst_base)
        instruccion = """
                         SELECT DISTINCT denominacion_del_proyecto, \
                            fecha_de_inicio, fecha_de_fin, cuantia_total, \
                            autores
                         FROM {0}_cvn_proyecto
                         WHERE (YEAR(fecha_de_inicio) = {1} OR \
                               (YEAR(fecha_de_inicio)<{1} AND \
                                YEAR(fecha_de_fin)>= {1}))
                         AND id IN (
                         {2})
                         ORDER BY fecha_de_inicio""".format("mem12", self.year,
                                                            inst_proyecto)
        cursor = self.db_connection.cursor()
        cursor.execute(instruccion)
        proyectos = cursor.fetchall()
        self.actividad["proyectos"] = proyectos'''

    def get_convenios(self):

        convenios = Convenio.objects.filter(usuario__in=self.investigadores) 
        #fecha_inicio = datetime.date(self.year, 12, 31)
        #fecha_fin = datetime.date(self.year, 1, 1)
        #convenios = convenios.filter(Q(fecha_inicio__isnull=False)&Q(fecha_inicio__lte=fecha_inicio))
        #investigadores = investigadores.filter(Q(cese__isnull=True)|Q(cese__gte=fecha_fin))
        return convenios
        '''inst_convenio = """
                        SELECT DISTINCT convenio_id
                        FROM {0}_cvn_convenio_usuario
                        WHERE usuario_id IN (
                            {1})""".format("mem12", self.inst_base)
        instruccion = """
                    SELECT DISTINCT denominacion_del_proyecto, \
                        fecha_de_inicio, cuantia_total, autores, \
                        duracion_anyos, duracion_meses, duracion_dias
                    FROM {0}_cvn_convenio
                    WHERE ((YEAR(fecha_de_inicio) = {1}) OR \
                           (duracion_anyos < 100 AND \
                            YEAR(INTERVAL (duracion_anyos * 365 + \
                                           duracion_meses * 12 + \
                                           duracion_dias) DAY + \
                                 fecha_de_inicio) >= {1})
                    OR
                    (duracion_anyos >= 100 AND \
                     YEAR(INTERVAL (duracion_meses * 12 + \
                                    duracion_dias) DAY + \
                          fecha_de_inicio) >= {1})
                    OR
                    (duracion_anyos >= {1})) AND id IN (
                    {2})
                    ORDER BY fecha_de_inicio""".format("mem12", self.year,
                                                       inst_convenio)
        cursor = self.db_connection.cursor()
        cursor.execute(instruccion)
        convenios = cursor.fetchall()
        self.actividad["convenios"] = convenios'''

    def get_tesis(self):
        #tesis_with_director = []
        return list(TesisDoctoral.objects.filter(Q(usuario__in=self.investigadores)&Q(fecha_de_lectura__year=self.year)))
        '''inst_tesis = """
                     SELECT DISTINCT tesisdoctoral_id
                     FROM {0}_cvn_tesisdoctoral_usuario
                     WHERE usuario_id IN (
                        {1})""".format("mem12", self.inst_base)
        instruccion = """
                      SELECT DISTINCT id, titulo, fecha_de_lectura, autor, \
                        universidad_que_titula, codirector
                      FROM {0}_cvn_tesisdoctoral
                      WHERE YEAR(fecha_de_lectura) = "{1}" AND
                            id IN (
                            {2})
                      ORDER BY fecha_de_lectura""".format("mem12", self.year,
                                                          inst_tesis)

        cursor = self.db_connection.cursor()
        cursor.execute(instruccion)
        all_tesis = cursor.fetchall()'''
        '''
        # añade datos del director de la tesis
        for tesis in all_tesis:
            id = tesis[0]
            inst_user = """
                        SELECT usuario_id
                        FROM {0}_cvn_tesisdoctoral_usuario
                        WHERE tesisdoctoral_id = {1}""".format("mem12", id)
            instruccion = """
                          SELECT nombre, primer_apellido, segundo_apellido
                          FROM {0}_cvn_usuario
                          WHERE id IN (
                          {1})""".format("mem12", inst_user)

            cursor = self.db_connection.cursor()
            cursor.execute(instruccion)
            director = cursor.fetchone()

            tesis_director = tesis + director
            tesis_with_director.append(tesis_director)

        self.actividad["tesis"] = tesis_with_director'''
