# -*- encoding: UTF-8 -*-

from PIL import Image  # needed to get the logo size
from slugify import slugify  # safe filename from string
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.platypus import (SimpleDocTemplate, Paragraph,
                                Spacer, Table, TableStyle)
from date_string_helpers import (getMonthText, cambia_fecha_a_normal,
                                 calcular_duracion, utf8)
import os


class Informe_pdf:
    """
    clase que genera un informe en formato PDF de un
        departamento: diccionario de datos
        investigadores: lista de tuplas con (nombre, primer apellido, i
                                             segundo apellido, categoria)
        produccion: diccionario: tipo de produccion (artículos, tesis,...)
         -> lista de tuplas
        actividad: diccionario: tipo de actividad (congresos, convenios...)
         -> lista de tuplas
    """
    DEFAULT_FONT = "Helvetica"
    DEPARTAMENTO_SIZE = 12
    SUBTITLE_STYLE = "<font size=11>"
    TEXT_SIZE = 10
    PAGE_NUMBERS_SIZE = 8
    MARGIN = inch
    PAGE_NUMBERS_MARGIN = 0.75 * MARGIN
    DEFAULT_SPACER = 0.3 * inch
    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]

    def __init__(self, year, departamento, investigadores, produccion,
                 actividad):
        self.year = year
        self.dept = departamento
        self.investigadores = investigadores
        self.produccion = produccion
        self.actividad = actividad

        self.logo()

    def logo(self):
        IMG_PATH = 'cvn/management/commands/images/'
        if os.path.exists(IMG_PATH + 'logo' + self.year + '.png'):
            LOGO = 'logo' + self.year + '.png'
        else:
            LOGO = 'logo.png'
        self.LOGO_PATH = IMG_PATH + LOGO

        self.LOGO_WIDTH, self.LOGO_HEIGHT = Image.open(self.LOGO_PATH).size

        LOGO_SCALE = 0.35
        self.LOGO_WIDTH *= LOGO_SCALE
        self.LOGO_HEIGHT *= LOGO_SCALE

    def styleN(self):
        style = getSampleStyleSheet()['Normal']
        style.leading = 24
        style.allowWidows = 0
        style.spaceBefore = 0.5 * inch
        return style

    def styleH3(self):
        style = getSampleStyleSheet()['Heading3']
        style.leading = 0
        style.allowWidows = 0
        style.spaceBefore = 0.5 * inch
        return style

    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        # Nombre del Departamento
        canvas.setFont(self.DEFAULT_FONT, self.DEPARTAMENTO_SIZE)
        canvas.drawString(self.MARGIN, self.PAGE_HEIGHT - 2 * self.MARGIN,
                          self.dept.nombre)
        # Logo
        canvas.drawImage(self.LOGO_PATH,
                         self.PAGE_WIDTH - self.MARGIN - self.LOGO_WIDTH,
                         self.PAGE_HEIGHT - self.LOGO_HEIGHT - self.MARGIN,
                         self.LOGO_WIDTH,
                         self.LOGO_HEIGHT)
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(self.DEFAULT_FONT, self.PAGE_NUMBERS_SIZE)
        canvas.drawCentredString(self.PAGE_WIDTH / 2.0,
                                 self.PAGE_NUMBERS_MARGIN,
                                 u"pág. {0} - {1}"
                                 .format(doc.page, self.dept.nombre))
        canvas.restoreState()

    def go(self):

        doc = SimpleDocTemplate(
            slugify(self.year + '-' + self.dept.nombre) + '.pdf'
        )

        Story = [Spacer(1, 3 * self.DEFAULT_SPACER)]

        Story.append(Spacer(1, 1 * self.DEFAULT_SPACER))

        # --------------------------------------------------------------------
        # INVESTIGADORES
        # --------------------------------------------------------------------
        Story.append(Paragraph('INVESTIGADORES', self.styleH3()))
        text = 'Número de investigadores: ' + str(len(self.investigadores))
        Story.append(Paragraph(text, self.styleN()))

        tablaInv = self.tablaInvestigadores()
        Story.append(tablaInv)
        Story.append(Spacer(1, 1 * self.DEFAULT_SPACER))
        # --------------------------------------------------------------------

        produccion = self.lista_produccion()
        for p in produccion:
            Story.append(p)

        #p = self.lista_congresos()
        #Story.append(p)

        #p = self.lista_proyectos()
        #Story.append(p)

        #p = self.lista_convenios()
        #Story.append(p)

        #p = self.lista_tesis()
        #Story.append(p)

        doc.build(Story, onFirstPage=self.myFirstPage,
                  onLaterPages=self.myLaterPages)

    def tablaInvestigadores(self):
        HEADERS = ["NOMBRE", "PRIMER APELLIDO", "SEGUNDO APELLIDO",
                   "CATEGORÍA"]
        data = [HEADERS] + self.investigadores
        tabla = Table(data, repeatRows=1)
        LIST_STYLE = TableStyle(
            [('SIZE', (0, 0), (-1, -1), 8),
             ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
             ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
             ('ALIGNMENT', (0, 0), (-1, 0), 'CENTER'),
             ('BACKGROUND', (0, 0), (-1, 0), colors.black),
             ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
             ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white,
                                                   colors.lightgrey]), ]
        )
        tabla.setStyle(LIST_STYLE)
        return tabla

    def lista_produccion(self):
        paragraphs = []
        for tipo_publicacion, publicaciones in self.produccion.items():
            num_publicaciones = len(publicaciones)
            if num_publicaciones > 0:
                paragraphs.append(self.lista_publicaciones(
                    tipo_publicacion, num_publicaciones, publicaciones))
        return paragraphs

    def lista_publicaciones(self, tipo_publicacion,
                            num_publicaciones, publicaciones):
        texto = "<b>{2}{0}</font> [{1}]</b><br/>".format(
            utf8(tipo_publicacion), num_publicaciones, self.SUBTITLE_STYLE)
        for publicacion in publicaciones:
            (fecha,
             titulo,
             nombre_publicacion,
             autores,
             issn,
             volumen,
             numero,
             pagina_inicial,
             pagina_final) = publicacion

            if fecha:
                fecha = cambia_fecha_a_normal(fecha)
                texto += "Fecha: {0}<br/>".format(utf8(fecha))

            if autores:
                texto += "{0}.".format(utf8(autores))

            if titulo:
                texto += " {0}".format(utf8(titulo))
                if titulo[-1] != ".":
                    texto += "."  # a veces el artículo lleva un punto final

            if nombre_publicacion:
                texto += " <i>{0}</i>".format(utf8(nombre_publicacion))

            if volumen:
                texto += ", vol {0}".format(utf8(volumen))

            if numero:
                texto += ", núm. {0}".format(utf8(numero))

            if pagina_inicial and pagina_final:
                texto += ", p. {0}-{1}".format(pagina_inicial, pagina_final)

            texto += ".<br/><br/>"  # punto final

        p = Paragraph(texto, self.styleN())
        return p

    def lista_congresos(self):
        congresos = self.actividad["congresos"]
        num_congresos = len(congresos)
        #print num_congresos
        texto = ""
        if num_congresos > 0:
            texto = "<b>{1}Comunicaciones a congresos </font>[{0}]</b><br/>"\
                .format(num_congresos, self.SUBTITLE_STYLE)
            for congreso in congresos:
                #print "Congreso:" , congreso
                (titulo, nombre_del_congreso, autores,
                 ciudad_de_realizacion, fecha_realizacion) = congreso
                if autores:
                    texto += "{0}.".format(utf8(autores))
                if titulo:
                    # FIXME change this to smart quotes
                    texto += ' "{0}"'.format(utf8(titulo))
                if nombre_del_congreso:
                    texto += " en: <i>{0}</i>".format(
                        utf8(nombre_del_congreso))
                mes = getMonthText(fecha_realizacion)
                if ciudad_de_realizacion and mes:
                    texto += ", ({0}, {1} de {2})".format(
                        utf8(ciudad_de_realizacion), mes, self.year)
                elif ciudad_de_realizacion:
                    texto += ", ({0})".format(utf8(ciudad_de_realizacion))
                elif mes:
                    texto += ", ({0} de {1})".format(mes, self.year)

                texto += ".<br/><br/>"  # punto final
            # end for congresos
        p = Paragraph(texto, self.styleN())
        return p

    def lista_proyectos(self):
        proyectos = self.actividad["proyectos"]
        num_proyectos = len(proyectos)
        #print num_proyectos
        texto = ""
        if num_proyectos > 0:
            texto = "<b>{2}Proyectos de investigación activos en {1} </font>"\
                    + "[{0}]</b><br/>".format(
                        num_proyectos, self.year, self.SUBTITLE_STYLE)
            for proyecto in proyectos:
                #print "Proyecto:" , proyecto
                (denominacion_del_proyecto, fecha_de_inicio,
                 fecha_de_fin, cuantia_total, autores) = proyecto
                # TODO revisar este orden
                if denominacion_del_proyecto:
                    texto += "Denominación: {0}.<br/>".format(
                        utf8(denominacion_del_proyecto))
                if fecha_de_inicio:
                    fecha_de_inicio = cambia_fecha_a_normal(fecha_de_inicio)
                    texto += "Fecha de inicio: {0}<br/>".format(
                        utf8(fecha_de_inicio))
                if fecha_de_fin:
                    fecha_de_fin = cambia_fecha_a_normal(fecha_de_fin)
                    texto += "Fecha de finalización: {0}<br/>".format(
                        utf8(fecha_de_fin))
                if cuantia_total:
                    texto += "Cuantía: {0}€<br/>".format(
                        utf8(unicode(cuantia_total)))
                if autores:
                    texto += "Investigadores: {0}<br/>".format(utf8(autores))
                texto += "<br/>"
            # end for proyectos
        p = Paragraph(texto, self.styleN())
        return p

    def lista_convenios(self):
        convenios = self.actividad["convenios"]
        num_convenios = len(convenios)
        #print num_convenios
        texto = ""
        if num_convenios > 0:
            texto = "<b>{2}Convenios de investigación activos en {1} "\
                    + "</font>[{0}]</b><br/>".format(num_convenios, self.year,
                                                     self.SUBTITLE_STYLE)
            for convenio in convenios:
                (denominacion_del_convenio, fecha_de_inicio, cuantia_total,
                 autores, duracion_anyos, duracion_meses,
                 duracion_dias) = convenio
                # TODO revisar este orden
                if denominacion_del_convenio:
                    texto += "Título: {0}.<br/>".format(utf8(
                        denominacion_del_convenio))
                if fecha_de_inicio:
                    new_fecha_de_inicio = cambia_fecha_a_normal(
                        fecha_de_inicio)
                    texto += "Fecha de inicio: {0}<br/>".format(
                        utf8(new_fecha_de_inicio))
                    fecha_de_fin = calcular_duracion(fecha_de_inicio,
                                                     duracion_anyos,
                                                     duracion_meses,
                                                     duracion_dias)
                    if fecha_de_fin > fecha_de_inicio:
                        fecha_de_fin = cambia_fecha_a_normal(fecha_de_fin)
                        texto += "Fecha de finalización: {0}<br/>".format(
                            utf8(fecha_de_fin))
                if cuantia_total:
                    texto += "Cuantía: {0}€<br/>".format(
                        utf8(unicode(cuantia_total)))
                if autores:
                    texto += "Investigadores: {0}<br/>".format(utf8(autores))
                texto += "<br/>"
            # end for convenios
        p = Paragraph(texto, self.styleN())
        return p

    def lista_tesis(self):
        tesis = self.actividad["tesis"]
        num_tesis = len(tesis)
        texto = ""
        if num_tesis > 0:
            texto = "<b>{1}Tesis doctorales</font> [{0}]</b><br/>".format(
                num_tesis, self.SUBTITLE_STYLE)
            for t in tesis:
                (id,
                 titulo,
                 fecha_de_lectura,
                 autor,
                 universidad_que_titula,
                 codirector,
                 dir_nombre,
                 dir_apellido1,
                 dir_apellido2) = t

                if autor:
                    texto += "Doctorando: {0}<br/>".format(utf8(autor))
                if universidad_que_titula:
                    texto += "Universidad que titula: {0}<br/>".format(
                        utf8(universidad_que_titula))

                if autor:
                    texto += "Título: {0}.<br/>".format(utf8(autor))

                if dir_apellido1:
                    texto += "Director: {0} {1} {2}<br/>".format(
                        utf8(dir_nombre), utf8(dir_apellido1),
                        utf8(dir_apellido2))

                if codirector:
                    texto += "Codirector: {0}<br/>".format(utf8(codirector))

                if fecha_de_lectura:
                    fecha_de_lectura = cambia_fecha_a_normal(fecha_de_lectura)
                    texto += "Fecha de lectura: {0}<br/>".format(
                        utf8(fecha_de_lectura))
                texto += "<br/>"
            # end for tesis
        p = Paragraph(texto, self.styleN())
        return p
