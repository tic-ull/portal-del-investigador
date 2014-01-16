# -*- encoding: utf8 -*-


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
    PRODUCCION = {u'Artículo': u'Artículos',
                  u'Libro': u'Libros',
                  u'Capítulo de Libro': u'Capítulos de libro'}

    def __init__(self, db_connection, identificador, year,
                 tipo="departamento"):
        self.db_connection = db_connection
        self.identificador = identificador
        self.year = year
        assert (tipo == "departamento" or tipo == "instituto")
        self.tipo = tipo
        self.setType()
        self.setTable()
        self.set_inst_base()

        self.datos_basicos = {}
        self.investigadores = []
        self.produccion = {}
        self.actividad = {}

    def setType(self):
        """
        Ajusta la variable de id para las consutas
        """
        self.tipo_id = self.tipo + "_id"  # necesario para las consultas

    def setTable(self):
        """
        ajusta la tabla de consulta para obtener los datos
        """
        self.table = "mem12_GrupoInvest_" + self.tipo

    def get_datos_basicos(self):
        """
        Consulta para obtener los datos del departamento/instituto especificado
        """
        instruccion = """SELECT nombre
                         FROM {0}
                         WHERE id = {1}""".format(self.table,
                                                  self.identificador)
        cursor = self.db_connection.cursor()
        cursor.execute(instruccion)
        row = cursor.fetchone()
        self.datos_basicos['nombre'] = row[0]
        # TODO
        # get more data with the web service and fill the dictionary
        return self.datos_basicos

    def get_investigadores(self):
        self.query_data_investigadores()
        return tuple(self.investigadores)

    def query_data_investigadores(self):
        """
        Datos de la Tabla de Investigadores del departamento/instituto
        """
        # Please Javier FIX THIS "mem12" thing
        instruccion = """SELECT DISTINCT nombre, apellido1, apellido2, nif
                         FROM {0}_GrupoInvest_investigador
                         WHERE {1} = {2}
                         ORDER BY apellido1""".format("mem12", self.tipo_id,
                                                      self.identificador)
        cursor = self.db_connection.cursor()
        cursor.execute(instruccion)
        rows = cursor.fetchall()
        # now adding the category and creating the list
        for investigador in rows:
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
            self.investigadores.append(investigador)

    def set_inst_base(self):
        self.inst_base = """
                            SELECT DISTINCT id
                            FROM {0}_cvn_usuario
                            WHERE documento IN (
                                SELECT DISTINCT nif
                                FROM {0}_GrupoInvest_investigador
                                WHERE {1} = {2})""".format("mem12",
                                                           self.tipo_id,
                                                           self.identificador)

    def dept_publicacion(self, tipo, instruccion_base):
        instruccion = u"""
                        SELECT DISTINCT fecha, titulo, nombre_publicacion, \
                            autores, issn, volumen, numero, pagina_inicial, \
                            pagina_final
                        FROM {0}_cvn_publicacion
                        WHERE YEAR(fecha) = {1} AND
                              tipo_de_produccion LIKE '{2}' AND
                              id IN ({3})
                        ORDER BY fecha""".format("mem12", self.year, tipo,
                                                 instruccion_base)
        return instruccion

    def get_produccion(self):
        """
        Para cada tipo de produccion realiza la consulta y rellena el
        diccionario
        """
        inst_publicacion = u"""
                            SELECT DISTINCT publicacion_id
                            FROM {0}_cvn_publicacion_usuario
                            WHERE usuario_id IN ({1})""".format("mem12",
                                                                self.inst_base)

        inst_tipo_public = u"""
                            SELECT id
                            FROM {0}_cvn_publicacion
                            WHERE id IN ({1})""".format("mem12",
                                                        inst_publicacion)

        for tipo, label in self.PRODUCCION.items():
            instruccion = self.dept_publicacion(tipo, inst_tipo_public)
            cursor = self.db_connection.cursor()
            cursor.execute(instruccion)
            publicaciones = cursor.fetchall()
            self.produccion[label] = publicaciones

        return self.produccion

    # Actividad Científica
    def get_actividad(self):
        self.dataCongresos()
        self.dataProyectos()
        self.dataConvenios()
        self.dataTesis()
        return self.actividad

    def dataCongresos(self):
        inst_congreso = """
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
        self.actividad["congresos"] = congresos

    def dataProyectos(self):
        inst_proyecto = """
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
        self.actividad["proyectos"] = proyectos

    def dataConvenios(self):
        inst_convenio = """
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
        self.actividad["convenios"] = convenios

    def dataTesis(self):
        tesis_with_director = []
        inst_tesis = """
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
        all_tesis = cursor.fetchall()

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

        self.actividad["tesis"] = tesis_with_director
