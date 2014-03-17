# -*- encoding: UTF-8 -*-

from django.core.management.base import BaseCommand, CommandError
from get_datos_departamento import Get_datos_departamento
from informe_pdf import Informe_pdf
from optparse import make_option
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

    def handle(self, *args, **options):
        self.checkArgs(options)
        self.create_report()

    def checkArgs(self, options):
        if not options['year']:
            raise CommandError("Option `--year=YYYY` must be specified.")
        else:
            self.year = options['year']

        if not options['id']:
            raise CommandError("Option `--id=X` must be specified.")
        else:
            self.deptID = options['id']

    def create_report(self):
        (departamento, investigadores, articulos,
         libros, capitulosLibro, congresos, proyectos,
         convenios, tesis) = self.getData()
        informe = Informe_pdf(self.year, departamento, investigadores,
                              articulos, libros, capitulosLibro,
                              congresos, proyectos, convenios, tesis)
        informe.go()

    def getData(self):
        dataDept = Get_datos_departamento(self.deptID, self.year)
        departamento = GrupoinvestDepartamento.objects.get(id=self.deptID)
        investigadores = dataDept.get_investigadores()
        articulos = dataDept.get_articulos()
        libros = dataDept.get_libros()
        capitulosLibro = dataDept.get_capitulos()
        congresos = dataDept.get_congresos()
        proyectos = dataDept.get_proyectos()
        convenios = dataDept.get_convenios()
        tesis = dataDept.get_tesis()
        return (departamento, investigadores, articulos,
                libros, capitulosLibro, congresos, proyectos,
                convenios, tesis)
