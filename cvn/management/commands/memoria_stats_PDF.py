# -*- encoding: UTF-8 -*-

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

# TODO: No funcionan por la conexión a la BBDD


class Command(BaseCommand):
    help = u'Genera las estadísticas de la memoria de investigación '\
           u'de un año. Usa una BBDD congelada accesible por SQL'
    option_list = BaseCommand.option_list + (
        make_option(
            "-y",
            "--year",
            dest="year",
            help="Specify year.",
        ),
        make_option(
            "-t",
            "--tbl",
            dest="tbl",
            help="Specify table for duplicate control",
        ),
    )

    SQL_PATH = 'cvn/management/commands/sql'  # está bien aquí?
    DEPARTAMENTOS_PATH = '/departamentos'
    CONSULTAS_DEPARTAMENTOS = {
        "/articulos_departamentos.sql": (
            "Artículos publicados en %s (por departamentos)"),
        "/capitulos_libros_departamentos.sql": (
            "Capítulos de libros publicados en %s (por departamentos)"),
        "/congresos_departamentos.sql": (
            "Congresos organizados en %s (por departamentos)"),
        "/convenios_departamentos.sql": (
            "Convenios vigentes en %s (por departamentos)"),
        "/investigadores_departamentos.sql": (
            "Investigadores en %s [***datos de 2013] (por departamentos)"),
        "/libros_departamentos.sql": (
            "Libros publicados en %s (por departamentos)"),
        "/proyectos_departamentos.sql": (
            "Proyectos en %s (por departamentos)"),
        "/publicaciones_departamentos.sql": (
            "Publicaciones en %s (por departamentos)"),
        "/tesis_departamentos.sql": (
            "Número de tesis leídas en %s (por departamentos)"),
    }

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        if options['year'] is None:
            raise CommandError("Option `--year=...` must be specified.")
        else:
            self.YEAR = options['year']

        self.create_stats()

    def create_stats(self):
        for sql_file, title in self.CONSULTAS_DEPARTAMENTOS.items():
            self.generate_stat(self.SQL_PATH + self.DEPARTAMENTOS_PATH +
                               sql_file, title)

    def generate_stat(self, sql_file, title):
        #print sql_file, title
        sql_query = " ".join(open(sql_file).readlines())
        cursor = self.CONNECTION.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()  # or fetchall()
        labels, values = [row[0] for row in rows], [row[1] for row in rows]
        print labels
        print values
        d = self.generate_horizontal_bar_chart(labels, values)
        from reportlab.graphics import renderPDF
        renderPDF.drawToFile(d, 'example1.pdf', title)

    def generate_horizontal_bar_chart(self, labels, values):
        """
        returns a drawing with a horizontal bar chart
        corresponding to the labesl and values passed
        TODO que quede bien en la página din A4.
            Cambiar los colores y el ángulo
        """

        from reportlab.lib import colors
        from reportlab.graphics.shapes import Drawing
        from reportlab.graphics.charts.barcharts import HorizontalBarChart
        drawing = Drawing(1000, 1414)  # con las proporciones de A4
        bc = HorizontalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 707
        bc.width = 500
        bc.data = [tuple(values)]
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 1414
        bc.valueAxis.valueStep = 10
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = labels
        drawing.add(bc)
        return drawing
