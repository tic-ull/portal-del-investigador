# -*- encoding: UTF-8 -*-

from cvn.models import (Articulo, Libro, Capitulo, Congreso, Proyecto,
                        Convenio, TesisDoctoral, UserProfile)
from cvn.utils import isdigit
from django.conf import settings as st
from django.core.management.base import BaseCommand, CommandError
from informe_pdf import Informe_pdf
from informe_csv import Informe_csv
from optparse import make_option
import simplejson as json
import urllib


class Command(BaseCommand):
    help = u'Genera un PDF/CSV con los datos de un Departamento/Area'
    option_list = BaseCommand.option_list + (
        make_option(
            "-y",
            "--year",
            dest="year",
            help="Specify the year in format YYYY",
        ),
        make_option(
            "-i",
            "--id",
            dest="id",
            help="Specify the ID of the Department/Area",
        ),
        make_option(
            "-t",
            "--type",
            dest="type",
            default='d',
            help="Specify the type of filtering: d (department) or a (area)",
        ),
        make_option(
            "-f",
            "--format",
            dest="format",
            default='pdf',
            help="Specify the output format",
        ),
    )

    def handle(self, *args, **options):
        self.checkArgs(options)
        year = int(options['year'])
        type_id = [int(options['id'])] if type(options['id']) is str else None
        model = None
        if options['type'] == 'a':
            # model = GrupoinvestAreaconocimiento
            self.model_type = 'area'
        else:
            self.model_type = 'departamento'
            self.codigo = 'cod_departamento'
        if options['format'] == 'pdf':
            self.generator = Informe_pdf
        else:
            self.generator = Informe_csv
        self.createReports(year, type_id, model)

    def checkArgs(self, options):
        if not isdigit(options['year']):
            raise CommandError(
                "Option `--year=YYYY` must exist and be a number")
        if (not isdigit(options['id'])) and options['id'] is not None:
            raise CommandError("Option `--id=X` must be a number")
        if not options['type'] == 'a' and not options['type'] == 'd':
            raise CommandError("Option `--type=X` must be a (area) "
                               "or d (department)")
        if not options['format'] == 'pdf' and not options['format'] == 'csv':
            raise CommandError("Option `--format=X` must be pdf or csv")

    def createReports(self, year, element_id, model):
        if element_id is None:
            if self.model_type == 'departamento':
                WS = '%sget_departamentos?ano=%s' % (
                    st.WS_SERVER_URL, year)
                elements = urllib.urlopen(WS).read()
                elements = elements.replace(
                    '[', '').replace(']', '').split(', ')
            else:
                elements = model.objects.all()
        else:
            elements = element_id

        for element in elements:
            if not element == 'INVES':
                if self.model_type == 'departamento':
                    WS = '%sget_info_departamento?cod_departamento=%s' % (
                        st.WS_SERVER_URL, element)
                    departamento = json.loads(urllib.urlopen(WS).read())
                    if departamento:
                        self.createReport(year, departamento)
                else:
                    self.createReport(year, element)

    def createReport(self, year, element):
        (investigadores, articulos,
         libros, capitulosLibro, congresos, proyectos,
         convenios, tesis) = self.getData(year, element)
        print 'Generando Informe para [%s] %s ... ' % (
            element[self.codigo], element['nombre'])
        if investigadores:
            informe = self.generator(year, element, investigadores,
                                     articulos, libros, capitulosLibro,
                                     congresos, proyectos, convenios, tesis,
                                     self.model_type)
            informe.go()
            print 'OK\n'
        else:
            print 'ERROR: No hay Investigadores\n'

    def getData(self, year, element):
        investigadores, usuarios = self.getInvestigadores(
            year, element
        )
        articulos = Articulo.objects.byUsuariosYear(usuarios, year)
        libros = Libro.objects.byUsuariosYear(usuarios, year)
        capitulosLibro = Capitulo.objects.byUsuariosYear(usuarios, year)
        congresos = Congreso.objects.byUsuariosYear(usuarios, year)
        proyectos = Proyecto.objects.byUsuariosYear(usuarios, year)
        convenios = Convenio.objects.byUsuariosYear(usuarios, year)
        tesis = TesisDoctoral.objects.byUsuariosYear(usuarios, year)
        return (investigadores, articulos,
                libros, capitulosLibro, congresos, proyectos,
                convenios, tesis)

    def getInvestigadores(self, year, element):
        WS = '%sget_pdi_vigente?cod_%s=%s&ano=%s' % (
            st.WS_SERVER_URL, self.model_type,
            element[self.codigo], year)
        invesRRHH = json.loads(urllib.urlopen(WS).read())
        inves = list()
        for inv in invesRRHH:
            WS = '%sget_info_pdi?cod_persona=%s&ano=%s' % (
                st.WS_SERVER_URL, inv, year)
            dataInv = json.loads(urllib.urlopen(WS).read())
            dataInv = self.checkInves(dataInv)
            inves.append(dataInv)
        investigadores = sorted(inves, key=lambda k: "%s %s" % (
            k['apellido1'], k['apellido2']))
        usuarios = UserProfile.objects.filter(rrhh_code__in=invesRRHH)
        return investigadores, usuarios

    def checkInves(self, inv):
        if 'nombre' not in inv:
            inv['nombre'] = ''
        if 'apellido1' not in inv:
            inv['apellido1'] = ''
        if 'apellido2' not in inv:
            inv['apellido2'] = ''
        if 'categoria' not in inv:
            inv['categoria'] = ''
        return inv
