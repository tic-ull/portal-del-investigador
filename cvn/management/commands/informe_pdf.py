# -*- encoding: UTF-8 -*-

from PIL import Image
from date_string_helpers import (cambia_fecha_a_normal, calcular_duracion,
                                 utf8)
from django.utils import translation
from django.utils.translation import ugettext
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle)
from slugify import slugify
import os


class Informe_pdf:
    DEFAULT_FONT = "Helvetica"
    DEPARTAMENTO_SIZE = 12
    SUBTITLE_STYLE = "<font size=11>"
    DEFAULT_SPACER = 0.1 * inch

    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]
    MARGIN = 10 * mm

    PAGE_NUMBERS_SIZE = 8
    PAGE_NUMBERS_MARGIN = 0.75 * MARGIN

    def __init__(self, year, departamento, investigadores, articulos,
                 libros, capitulosLibro, congresos, proyectos):
        self.year = year
        self.departamento = departamento
        self.investigadores = investigadores
        self.articulos = articulos
        self.libros = libros
        self.capitulosLibro = capitulosLibro
        self.congresos = congresos
        self.proyectos = proyectos
        self.setLogo()

    def setLogo(self):
        img_path = 'cvn/management/commands/images/'
        if not os.path.exists(img_path + 'logo' + self.year + '.png'):
            logo = 'logo.png'
        else:
            logo = 'logo' + self.year + '.png'
        self.logo_path = img_path + logo

        self.logo_width, self.logo_height = Image.open(self.logo_path).size

        logo_scale = 0.35
        self.logo_width *= logo_scale
        self.logo_height *= logo_scale

    def go(self):
        doc = SimpleDocTemplate(
            slugify(self.year + '-' + self.departamento.nombre) + '.pdf'
        )
        story = [Spacer(1, 3 * self.DEFAULT_SPACER)]

        if self.investigadores:
            self.showInvestigadores(story)
            story.append(Spacer(1, 1 * self.DEFAULT_SPACER))

        if self.articulos:
            self.showArticulos(story)
            story.append(Spacer(1, 1 * self.DEFAULT_SPACER))

        if self.libros:
            self.showLibros(story)
            story.append(Spacer(1, 1 * self.DEFAULT_SPACER))

        if self.congresos:
            self.showCongresos(story)
            story.append(Spacer(1, 1 * self.DEFAULT_SPACER))

        if self.proyectos:
            self.showProyectos(story)
            story.append(Spacer(1, 1 * self.DEFAULT_SPACER))

        doc.build(story, onFirstPage=self.firstPage,
                  onLaterPages=self.laterPages)

    # -------------------------------------------------------------------------
    # PROCESADO DE LOS DATOS
    # -------------------------------------------------------------------------

    def showInvestigadores(self, story):
        story.append(Paragraph('INVESTIGADORES', self.styleH3()))
        text = 'Número de investigadores: ' + str(len(self.investigadores))
        story.append(Paragraph(text, self.styleN()))
        story.append(self.tableInvestigadores())

    def tableInvestigadores(self):
        HEADERS = ["NOMBRE", "PRIMER APELLIDO", "SEGUNDO APELLIDO",
                   "CATEGORÍA"]
        data = [HEADERS] + self.investigadores
        table = Table(data, repeatRows=1)
        table.setStyle(self.styleTable())
        return table

    # -------------------------------------------------------------------------

    def showArticulos(self, story):
        story.append(Paragraph('ARTÍCULOS', self.styleH3()))
        text = 'Número de artículos: ' + str(len(self.articulos))
        story.append(Paragraph(text, self.styleN()))
        self.listArticulos(story)

    def listArticulos(self, story):
        for art in self.articulos:
            text = ""
            if art.fecha:
                text += u"<b>Fecha:</b> %s <br/>" % (
                    art.fecha.strftime("%d/%m/%Y")
                )
            if art.titulo:
                text += u"<b>%s</b><br/>" % (art.titulo)
            if art.autores:
                text += u"%s<br/>" % (art.autores)
            if art.nombre_publicacion:
                text += u"%s<br/>" % (art.nombre_publicacion)
            if art.volumen:
                text += u"Vol. %s, " % (art.volumen)
            if art.numero:
                text += u"Núm. %s, " % (art.numero)
            if art.pagina_inicial and art.pagina_final:
                text += u"Pág. %s-%s" % (
                    art.pagina_inicial,
                    art.pagina_final
                )
            if art.issn:
                text += u" - ISSN: %s" % (art.issn)
            story.append(Paragraph(text, self.styleN()))

    # -------------------------------------------------------------------------

    def showLibros(self, story):
        story.append(Paragraph('LIBROS', self.styleH3()))
        text = 'Número de libros: ' + str(len(self.libros))
        story.append(Paragraph(text, self.styleN()))
        self.listLibros(story)

    def listLibros(self, story):
        for libro in self.libros:
            text = ""
            if libro.fecha:
                text += u"<b>Fecha:</b> %s <br/>" % (
                    libro.fecha.strftime("%d/%m/%Y")
                )
            if libro.titulo:
                text += u"<b>%s</b><br/>" % (libro.titulo)
            if libro.autores:
                text += u"%s<br/>" % (libro.autores)
            if libro.nombre_publicacion:
                text += u"%s <br/>" % (libro.nombre_publicacion)
            if libro.isbn:
                text += u"ISBN: %s" % (libro.isbn)
            story.append(Paragraph(text, self.styleN()))

    # -------------------------------------------------------------------------

    def showCapitulosLibro(self, story):
        story.append(Paragraph('CAPÍTULOS DE LIBROS', self.styleH3()))
        text = 'Número de capítulos de libros: ' + str(len(self.libros))
        story.append(Paragraph(text, self.styleN()))
        self.listLibros(story)

    def listCapitulosLibro(self, story):
        for capLibro in self.capitulosLibro:
            text = ""
            if capLibro.fecha:
                text += u"<b>Fecha:</b> %s <br/>" % (
                    capLibro.fecha.strftime("%d/%m/%Y")
                )
            if capLibro.titulo:
                text += u"<b>%s</b><br/>" % (capLibro.titulo)
            if capLibro.autores:
                text += u"%s<br/>" % (capLibro.autores)
            if capLibro.nombre_publicacion:
                text += u"%s " % (capLibro.nombre_publicacion)
            if capLibro.pagina_inicial and capLibro.pagina_final:
                text += u"Pág. %s-%s" % (
                    capLibro.pagina_inicial,
                    capLibro.pagina_final
                )
            if capLibro.isbn:
                text += u" - ISBN: %s" % (capLibro.isbn)
            story.append(Paragraph(text, self.styleN()))

    # -------------------------------------------------------------------------

    def showCongresos(self, story):
        story.append(Paragraph('COMUNICACIONES EN CONGRESOS', self.styleH3()))
        text = 'Número de comunicaciones en congresos: ' + str(
            len(self.congresos)
        )
        story.append(Paragraph(text, self.styleN()))
        self.listCongresos(story)

    def listCongresos(self, story):
        translation.activate('es')
        for congreso in self.congresos:
            text = ""
            if congreso.titulo:
                text += u"<b>%s</b><br/>" % (congreso.titulo)
            if congreso.nombre_del_congreso:
                text += u"%s " % (congreso.nombre_del_congreso)
            if congreso.ciudad_de_realizacion and congreso.fecha_realizacion:
                translation.activate('es')
                text += "(%s, %s de %s)<br/>" % (
                    congreso.ciudad_de_realizacion,
                    ugettext(congreso.fecha_realizacion.strftime("%B")),
                    congreso.fecha_realizacion.strftime("%Y")
                )
            elif congreso.ciudad_de_realizacion:
                text += "(%s)<br/>" % congreso.ciudad_de_realizacion
            elif congreso.fecha_realizacion:
                text += "(%s)<br/>" % congreso.fecha_realizacion
            if congreso.autores:
                text += u"%s" % (congreso.autores)
            story.append(Paragraph(text, self.styleN()))
        translation.deactivate()

    # -------------------------------------------------------------------------

    def showProyectos(self, story):
        story.append(Paragraph('PROYECTOS ACTIVOS', self.styleH3()))
        text = 'Número de proyectos activos: ' + str(
            len(self.proyectos)
        )
        story.append(Paragraph(text, self.styleN()))
        self.listProyectos(story)

    def listProyectos(self, story):
        for proy in self.proyectos:
            text = ""
            if proy.denominacion_del_proyecto:
                text += u"<b>%s</b><br/>" % (proy.denominacion_del_proyecto)
            if proy.fecha_de_inicio:
                text += u"Fecha de inicio: %s<br/>" % (
                    proy.fecha_de_inicio.strftime("%d/%m/%Y")
                )
            if proy.fecha_de_fin:
                text += u"Fecha de finalización: %s<br/>" % (
                    proy.fecha_de_fin.strftime("%d/%m/%Y")
                )
            if proy.cuantia_total:
                text += u"Cuantía: %s<br/>" % (proy.cuantia_total)
            if proy.autores:
                text += u"Investigadores: %s" % (proy.autores)
            story.append(Paragraph(text, self.styleN()))

    # -------------------------------------------------------------------------

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

    # -------------------------------------------------------------------------
    # CONFIGURACIÓN DE LAS PÁGINAS
    # -------------------------------------------------------------------------

    def firstPage(self, canvas, doc):
        canvas.saveState()
        self.header(canvas)
        canvas.restoreState()

    def laterPages(self, canvas, doc):
        canvas.saveState()
        self.header(canvas)
        canvas.setFont(self.DEFAULT_FONT, self.PAGE_NUMBERS_SIZE)
        canvas.drawCentredString(self.PAGE_WIDTH / 2.0,
                                 self.PAGE_NUMBERS_MARGIN,
                                 u'Página %s - %s' % (
                                     doc.page,
                                     self.departamento.nombre
                                 ))
        canvas.restoreState()

    def header(self, canvas):
        # Nombre del Departamento
        canvas.setFont(self.DEFAULT_FONT, self.DEPARTAMENTO_SIZE)
        canvas.drawString(self.MARGIN, self.PAGE_HEIGHT - 2 * self.MARGIN,
                          self.departamento.nombre)
        # Logo
        canvas.drawImage(self.logo_path,
                         self.PAGE_WIDTH - self.MARGIN - self.logo_width,
                         self.PAGE_HEIGHT - self.logo_height - self.MARGIN,
                         self.logo_width,
                         self.logo_height)

    # --------------------------------------------------------------------
    # ESTILOS DEL PDF
    # --------------------------------------------------------------------

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
        return style

    def styleTable(self):
        style = TableStyle(
            [('SIZE', (0, 0), (-1, -1), 8),
             ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
             ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
             ('ALIGNMENT', (0, 0), (-1, 0), 'CENTER'),
             ('BACKGROUND', (0, 0), (-1, 0), colors.black),
             ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
             ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white,
                                                   colors.lightgrey]), ]
        )
        return style
