# -*- encoding: UTF-8 -*-

from core.models import UserProfile
from core.ws_utils import CachedWS as ws
from cvn.models import (Articulo, Libro, Capitulo, Congreso, Proyecto,
                        Convenio, TesisDoctoral, Patente)
from cvn.utils import isdigit
from django.conf import settings as st
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from informe_csv import InformeCSV
from informe_pdf import InformePDF
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
        unit_id = [int(options['id'])] if type(options['id']) is str else None
        model = None
        if options['type'] == 'a':
            self.model_type = 'area'
        else:
            self.model_type = 'department'
        if options['format'] == 'pdf':
            self.generator = InformePDF
        else:
            self.generator = InformeCSV
        self.create_reports(year, unit_id, model)

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

    def create_reports(self, year, unit_id, model):
        if unit_id is None:
            if self.model_type == 'department':
                units = ws.get(st.WS_DEPARTMENTS_AND_MEMBERS_YEAR % year)
            else:
                units = ws.get(st.WS_AREAS_AND_MEMBERS_YEAR % year)
            if units is None:
                raise IOError('WS does not work')
            for unit in units:
                self.create_report(year, unit)
        else:
            for code in unit_id:
                if self.model_type == 'department':
                    unit = ws.get(st.WS_DEPARTMENTS_AND_MEMBERS_UNIT_YEAR % (
                        code, year))
                else:
                    unit = ws.get(st.WS_AREAS_AND_MEMBERS_UNIT_YEAR % (
                        code, year))
                if unit is not None:
                    self.create_report(year, unit.pop())

    def create_report(self, year, unit):
        (investigadores, articulos,
         libros, capitulos_libro, congresos, proyectos,
         convenios, tesis, patentes) = self.get_data(year, unit)
        print 'Generando Informe para [%s] %s ... ' % (
            unit['unidad']['codigo'], unit['unidad']['nombre'])
        if investigadores:
            informe = self.generator(year, unit['unidad'], investigadores,
                                     articulos, libros, capitulos_libro,
                                     congresos, proyectos, convenios, tesis,
                                     patentes, self.model_type)
            informe.go()
            print 'OK\n'
        else:
            print 'ERROR: No hay Investigadores\n'

    def get_data(self, year, unit):
        investigadores, usuarios = self.get_investigadores(unit)
        articulos = Articulo.objects.byUsuariosYear(usuarios, year)
        libros = Libro.objects.byUsuariosYear(usuarios, year)
        capitulos_libro = Capitulo.objects.byUsuariosYear(usuarios, year)
        congresos = Congreso.objects.byUsuariosYear(usuarios, year)
        proyectos = Proyecto.objects.byUsuariosYear(usuarios, year)
        convenios = Convenio.objects.byUsuariosYear(usuarios, year)
        tesis = TesisDoctoral.objects.byUsuariosYear(usuarios, year)
        patentes = Patente.objects.byUsuariosYear(usuarios, year)
        return (investigadores, articulos,
                libros, capitulos_libro, congresos, proyectos,
                convenios, tesis, patentes)

    def get_investigadores(self, unit):
        investigadores = list()
        usuarios = list()
        for inv in unit['miembros']:
            inv = self.check_inves(inv)
            investigadores.append(inv)
            try:
                user = UserProfile.objects.get(rrhh_code=inv['cod_persona'])
                usuarios.append(user)
            except ObjectDoesNotExist:
                pass
        return investigadores, usuarios

    def check_inves(self, inv):
        if 'cod_persona__nombre' not in inv:
            inv['cod_persona__nombre'] = ''
        if 'cod_persona__apellido1' not in inv:
            inv['cod_persona__apellido1'] = ''
        if 'cod_persona__apellido2' not in inv:
            inv['cod_persona__apellido2'] = ''
        if 'cod_cce__descripcion' not in inv:
            inv['cod_cce_descripcion'] = ''
        return inv
