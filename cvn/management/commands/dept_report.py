# -*- encoding: utf8 -*-

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from get_datos_departamento import Get_datos_departamento
from informe_pdf import Informe_pdf
from viinvDB.models import GrupoinvestDepartamento


class Command(BaseCommand):
    help = u'Genera un PDF con los datos de un Departamento'
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
            help="Specify the ID of the Department",
        ),
    )

    def checkArgs(self, options):
        if not options['year']:
            raise CommandError("Option `--year=YYYY` must be specified.")
        else:
            self.YEAR = options['year']

        if not options['id']:
            raise CommandError("Option `--id=X` must be specified.")
        else:
            self.ID = options['id']

    def handle(self, *args, **options):
        self.checkArgs(options)
        self.create_report()

    def create_report(self):
        data_dept = Get_datos_departamento(self.ID, self.YEAR)
        dept = GrupoinvestDepartamento.objects.get(id=self.ID)
        invs = data_dept.get_investigadores()
        produccion = {}  # data_dept.get_produccion()
        actividad = {}  # data_dept.get_actividad()
        informe = Informe_pdf(self.YEAR, dept, invs, produccion, actividad)
        informe.go()
