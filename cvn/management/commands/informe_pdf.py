# -*- encoding: UTF-8 -*-

from PIL import Image
from cvn import settings as st_cvn
from django.utils import translation
from django.utils.translation import ugettext
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle)
from reportlab.platypus.flowables import PageBreak
from slugify import slugify
import os


class Informe_pdf:
    BLUE_SECONDARY_ULL = colors.HexColor('#EBF3FA')
    BLUE_ULL = colors.HexColor('#006699')
    DEFAULT_FONT = 'Helvetica'
    DEFAULT_FONT_BOLD = 'Helvetica-Bold'
    DEFAULT_SPACER = 0.1 * inch
    HEADER_FONT_SIZE = 14
    MARGIN = 10 * mm
    PAGE_HEIGHT = A4[1]
    PAGE_NUMBERS_MARGIN = 0.75 * MARGIN
    PAGE_NUMBERS_SIZE = 8
    PAGE_WIDTH = A4[0]
    VIOLET_ULL = colors.HexColor('#7A3B7A')

    def __init__(self, year, departamento, investigadores, articulos, libros,
                 capitulos_libro, congresos, proyectos, convenios, tesis,
                 model_type=None):
        self.year = str(year)
        self.departamento = departamento
        self.investigadores = investigadores
        self.articulos = articulos
        self.libros = libros
        self.capitulosLibro = capitulos_libro
        self.congresos = congresos
        self.proyectos = proyectos
        self.convenios = convenios
        self.tesis = tesis
        self.setLogo()

    def setLogo(self):
        img_path = st_cvn.PDF_DEPT_IMAGES
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
        path_file = "%s/%s/" % (st_cvn.PDF_DEPT_ROOT, self.year)
        if not os.path.isdir(path_file):
            os.makedirs(path_file)
        file_name = slugify(
            self.year + "-" + self.departamento['nombre']) + ".pdf"
        doc = SimpleDocTemplate(path_file + file_name)
        story = [Spacer(1, 3 * self.DEFAULT_SPACER)]
        if self.investigadores:
            self.showInvestigadores(story)
        if self.articulos:
            self.showArticulos(story)
        if self.libros:
            self.showLibros(story)
        if self.capitulosLibro:
            self.showCapitulosLibro(story)
        if self.congresos:
            self.showCongresos(story)
        if self.proyectos:
            self.showProyectos(story)
        if self.convenios:
            self.showConvenios(story)
        if self.tesis:
            self.showTesis(story)
        doc.build(story, onFirstPage=self.firstPage,
                  onLaterPages=self.laterPages)

    # -------------------------------------------------------------------------
    # PROCESADO DE LOS DATOS
    # -------------------------------------------------------------------------

    def showInvestigadores(self, story):
        story.append(Paragraph('INVESTIGADORES', self.styleH3()))
        text = 'Número de investigadores: ' + str(len(self.investigadores))
        story.append(Paragraph(text, self.styleN()))
        story.append(Spacer(1, 1 * self.DEFAULT_SPACER))
        story.append(self.tableInvestigadores())

    def tableInvestigadores(self):
        table_inv = []
        for inv in self.investigadores:
            table_inv.append([
                inv['nombre'],
                inv['apellido1'],
                inv['apellido2'],
                inv['categoria']])
        HEADERS = ["NOMBRE", "PRIMER APELLIDO", "SEGUNDO APELLIDO",
                   "CATEGORÍA"]
        data = [HEADERS] + table_inv
        table = Table(data, repeatRows=1)
        table.setStyle(self.styleTable())
        return table

    # -------------------------------------------------------------------------

    def showArticulos(self, story):
        story.append(PageBreak())
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
                text += u"<b>%s</b><br/>" % art.titulo
            if art.autores:
                text += u"%s<br/>" % art.autores
            if art.nombre_publicacion:
                text += u"%s<br/>" % art.nombre_publicacion
            if art.volumen:
                text += u"Vol. %s &nbsp; &nbsp;" % art.volumen
            if art.numero:
                text += u"Núm. %s &nbsp; &nbsp;" % art.numero
            if art.pagina_inicial and art.pagina_final:
                text += u"Pág. %s-%s &nbsp; &nbsp;" % (
                    art.pagina_inicial,
                    art.pagina_final
                )
            if art.issn:
                text += u"ISSN: %s" % art.issn
            story.append(Paragraph(text, self.styleN()))

    # -------------------------------------------------------------------------

    def showLibros(self, story):
        story.append(PageBreak())
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
                text += u"<b>%s</b><br/>" % libro.titulo
            if libro.autores:
                text += u"%s<br/>" % libro.autores
            if libro.nombre_publicacion:
                text += u"%s<br/>" % libro.nombre_publicacion
            if libro.isbn:
                text += u"ISBN: %s" % libro.isbn
            story.append(Paragraph(text, self.styleN()))

    # -------------------------------------------------------------------------

    def showCapitulosLibro(self, story):
        story.append(PageBreak())
        story.append(Paragraph('CAPÍTULOS DE LIBROS', self.styleH3()))
        text = 'Número de capítulos de libros: ' + str(
            len(self.capitulosLibro)
        )
        story.append(Paragraph(text, self.styleN()))
        self.listCapitulosLibro(story)

    def listCapitulosLibro(self, story):
        for capLibro in self.capitulosLibro:
            text = ""
            if capLibro.fecha:
                text += u"<b>Fecha:</b> %s <br/>" % (
                    capLibro.fecha.strftime("%d/%m/%Y")
                )
            if capLibro.titulo:
                text += u"<b>%s</b><br/>" % capLibro.titulo
            if capLibro.autores:
                text += u"%s<br/>" % capLibro.autores
            if capLibro.nombre_publicacion:
                text += u"%s &nbsp; &nbsp;" % capLibro.nombre_publicacion
            if capLibro.pagina_inicial and capLibro.pagina_final:
                text += u"Pág. %s-%s &nbsp; &nbsp;" % (
                    capLibro.pagina_inicial,
                    capLibro.pagina_final
                )
            if capLibro.isbn:
                text += u"ISBN: %s" % capLibro.isbn
            story.append(Paragraph(text, self.styleN()))

    # -------------------------------------------------------------------------

    def showCongresos(self, story):
        story.append(PageBreak())
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
                text += u"<b>%s</b><br/>" % congreso.titulo
            if congreso.nombre_del_congreso:
                text += u"%s " % congreso.nombre_del_congreso
            if congreso.ciudad_de_realizacion and congreso.fecha_de_inicio:
                translation.activate('es')
                text += "(%s, %s de %s)<br/>" % (
                    congreso.ciudad_de_realizacion,
                    ugettext(congreso.fecha_de_inicio.strftime("%B")),
                    congreso.fecha_de_inicio.strftime("%Y")
                )
            elif congreso.ciudad_de_realizacion:
                text += "(%s)<br/>" % congreso.ciudad_de_realizacion
            elif congreso.fecha_de_inicio:
                text += "(%s)<br/>" % congreso.fecha_de_inicio
            if congreso.autores:
                text += u"%s" % congreso.autores
            story.append(Paragraph(text, self.styleN()))
        translation.deactivate()

    # -------------------------------------------------------------------------

    def showProyectos(self, story):
        story.append(PageBreak())
        story.append(Paragraph('PROYECTOS ACTIVOS', self.styleH3()))
        text = 'Número de proyectos activos: ' + str(
            len(self.proyectos)
        )
        story.append(Paragraph(text, self.styleN()))
        self.listProyectos(story)

    def listProyectos(self, story):
        for proy in self.proyectos:
            text = ""
            if proy.titulo:
                text += u"<b>%s</b><br/>" % proy.titulo
            if proy.fecha_de_inicio:
                text += u"Fecha de inicio: %s<br/>" % (
                    proy.fecha_de_inicio.strftime("%d/%m/%Y")
                )
            if proy.fecha_de_fin:
                text += u"Fecha de finalización: %s<br/>" % (
                    proy.fecha_de_fin.strftime("%d/%m/%Y")
                )
            if proy.cuantia_total:
                text += u"Cuantía: %s<br/>" % proy.cuantia_total
            if proy.autores:
                text += u"Investigadores: %s" % proy.autores
            story.append(Paragraph(text, self.styleN()))

    # -------------------------------------------------------------------------

    def showConvenios(self, story):
        story.append(PageBreak())
        story.append(Paragraph('CONVENIOS ACTIVOS', self.styleH3()))
        text = 'Número de convenios activos: ' + str(
            len(self.convenios)
        )
        story.append(Paragraph(text, self.styleN()))
        self.listConvenios(story)

    def listConvenios(self, story):
        for conv in self.convenios:
            text = ""
            if conv.titulo:
                text += u"<b>%s</b><br/>" % conv.titulo
            if conv.fecha_de_inicio:
                text += u"Fecha de inicio: %s<br/>" % (
                    conv.fecha_de_inicio.strftime("%d/%m/%Y")
                )
            text += u"Fecha de finalización: %s<br/>" % (
                    conv.fecha_de_fin.strftime("%d/%m/%Y")
                )
            if conv.cuantia_total:
                text += u"Cuantía: %s<br/>" % conv.cuantia_total
            if conv.autores:
                text += u"Investigadores: %s" % conv.autores
            story.append(Paragraph(text, self.styleN()))

    # -------------------------------------------------------------------------

    def showTesis(self, story):
        story.append(PageBreak())
        story.append(Paragraph('TESIS DOCTORALES', self.styleH3()))
        text = 'Número de tesis doctorales: ' + str(
            len(self.tesis)
        )
        story.append(Paragraph(text, self.styleN()))
        self.listTesis(story)

    def listTesis(self, story):
        for t in self.tesis:
            text = ""
            if t.titulo:
                text += u"<b>%s</b><br/>" % t.titulo
            if t.autor:
                text += u"Doctorando: %s<br/>" % t.autor
            if t.universidad_que_titula:
                text += u"Universidad: %s<br/>" % (
                    t.universidad_que_titula
                )
            if t.usuario:
                text += u"Director: %s" % t.usuario
            if t.codirector:
                text += u"Codirector: %s" % t.codirector
            if t.fecha:
                text += u"Fecha de lectura: %s<br/>" % (
                    t.fecha.strftime("%d/%m/%Y")
                )
            story.append(Paragraph(text, self.styleN()))

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
                                     self.departamento['nombre']
                                 ))
        canvas.restoreState()

    def header(self, canvas):
        canvas.setFont(self.DEFAULT_FONT_BOLD, self.HEADER_FONT_SIZE)
        canvas.setFillColor(self.BLUE_ULL)
        canvas.drawString(self.MARGIN, self.PAGE_HEIGHT - 2 * self.MARGIN,
                          self.departamento['nombre'])
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
        style.leading = 12
        style.allowWidows = 0
        style.spaceBefore = 0.5 * inch
        return style

    def styleH3(self):
        style = getSampleStyleSheet()['Heading3']
        style.textColor = self.VIOLET_ULL
        return style

    def styleTable(self):
        style = TableStyle(
            [('SIZE', (0, 0), (-1, -1), 8),
             ('BOX', (0, 0), (-1, -1), 0.2, self.BLUE_ULL),
             ('LINEABOVE', (0, 0), (-1, -1), 0.2, self.BLUE_ULL),
             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
             ('BACKGROUND', (0, 0), (-1, 0), self.BLUE_ULL),
             ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
             ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white,
                                                   self.BLUE_SECONDARY_ULL])]
        )
        return style
