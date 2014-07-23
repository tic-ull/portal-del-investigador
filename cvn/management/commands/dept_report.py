# -*- encoding: UTF-8 -*-

from core.redis_utils import wsget
from cvn.models import (Articulo, Libro, Capitulo, Congreso, Proyecto,
                        Convenio, TesisDoctoral, UserProfile)
from cvn.utils import isdigit
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as st
from informe_pdf import Informe_pdf
from informe_csv import Informe_csv
from optparse import make_option


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
        self.check_args(options)
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
        self.create_reports(year, type_id, model)

    def check_args(self, options):
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

    def create_reports(self, year, element_id, model):
        if element_id is None:
            if self.model_type == 'departamento':
                elements = wsget(st.WS_CODES_DEPARTMENTS_YEAR % year)
                if elements is None:
                    raise IOError('WS "%s" does not work' %
                                  st.WS_CODES_DEPARTMENTS_YEAR % year)
                elements = elements.replace(
                    '[', '').replace(']', '').split(', ')
            else:
                elements = model.objects.all()
        else:
            elements = element_id

        for element in elements:
            if not element == 'INVES':
                if self.model_type == 'departamento':
                    departamento = wsget(st.WS_INFO_DEPARTMENT % element)
                    if departamento:
                        self.create_report(year, departamento)
                else:
                    self.create_report(year, element)

    def create_report(self, year, element):
        (investigadores, articulos,
         libros, capitulos_libro, congresos, proyectos,
         convenios, tesis) = self.get_data(year, element)
        print 'Generando Informe para [%s] %s ... ' % (
            element[self.codigo], element['nombre'])
        if investigadores:
            informe = self.generator(year, element, investigadores,
                                     articulos, libros, capitulos_libro,
                                     congresos, proyectos, convenios, tesis,
                                     self.model_type)
            informe.go()
            print 'OK\n'
        else:
            print 'ERROR: No hay Investigadores\n'

    def get_data(self, year, element):
        investigadores, usuarios = self.get_investigadores(
            year, element
        )
        articulos = Articulo.objects.byUsuariosYear(usuarios, year)
        libros = Libro.objects.byUsuariosYear(usuarios, year)
        capitulos_libro = Capitulo.objects.byUsuariosYear(usuarios, year)
        congresos = Congreso.objects.byUsuariosYear(usuarios, year)
        proyectos = Proyecto.objects.byUsuariosYear(usuarios, year)
        convenios = Convenio.objects.byUsuariosYear(usuarios, year)
        tesis = TesisDoctoral.objects.byUsuariosYear(usuarios, year)
        return (investigadores, articulos,
                libros, capitulos_libro, congresos, proyectos,
                convenios, tesis)

    def get_investigadores(self, year, element):
        inves_rrhh = wsget(st.WS_PDI_VALID_UNIDAD_YEAR % (
            self.model_type, element[self.codigo], year))
        if inves_rrhh is None:
            raise IOError('WS "%s" does not work' %
                          (st.WS_PDI_VALID_UNIDAD_YEAR % (
                           self.model_type, element[self.codigo], year)))
        inves = list()
        for inv in inves_rrhh:
            data_inv = wsget(st.WS_INFO_PDI_YEAR % inv, year)
            if data_inv is None:
                raise IOError('WS "%s" does not work' %
                              st.WS_INFO_PDI_YEAR % inv, year)
            data_inv = self.check_inves(data_inv)
            inves.append(data_inv)
        investigadores = sorted(inves, key=lambda k: "%s %s" % (
            k['apellido1'], k['apellido2']))
        usuarios = UserProfile.objects.filter(rrhh_code__in=inves_rrhh)
        return investigadores, usuarios

    def check_inves(self, inv):
        if 'nombre' not in inv:
            inv['nombre'] = ''
        if 'apellido1' not in inv:
            inv['apellido1'] = ''
        if 'apellido2' not in inv:
            inv['apellido2'] = ''
        if 'categoria' not in inv:
            inv['categoria'] = ''
        return inv
