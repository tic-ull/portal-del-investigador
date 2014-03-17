# -*- encoding: UTF-8 -*-

from cvn.models import Publicacion, Congreso, Proyecto, Convenio, TesisDoctoral
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
        usuarios = dataDept.get_usuarios()
        departamento = GrupoinvestDepartamento.objects.get(id=self.deptID)
        investigadores = dataDept.get_investigadores()
        articulos = Publicacion.objects.byUsuariosYearTipo(
            usuarios, self.year, 'Artículo'
        )
        libros = Publicacion.objects.byUsuariosYearTipo(
            usuarios, self.year, 'Libro'
        )
        capitulosLibro = Publicacion.objects.byUsuariosYearTipo(
            usuarios, self.year, 'Capítulo de Libro'
        )
        congresos = Congreso.objects.byUsuariosYear(usuarios, self.year)
        proyectos = Proyecto.objects.byUsuariosYear(usuarios, int(self.year))
        convenios = Convenio.objects.byUsuariosYear(usuarios, int(self.year))
        tesis = TesisDoctoral.objects.byUsuariosYear(usuarios, self.year)
        return (departamento, investigadores, articulos,
                libros, capitulosLibro, congresos, proyectos,
                convenios, tesis)
