# -*- encoding: UTF-8 -*-

from cvn.models import (Publicacion, Congreso, Proyecto, Convenio,
                        TesisDoctoral, Usuario)
from cvn.utils import isdigit
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from informe_pdf import Informe_pdf
from optparse import make_option
from viinvDB.models import GrupoinvestDepartamento, GrupoinvestInvestigador
import datetime

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
        year = int(options['year'])
        departamentos = [int(options['id'])] if type(options['id']) is str else None
        self.create_reports(year, departamentos)

    def checkArgs(self, options):
        if not isdigit(options['year']):
            raise CommandError(
                "Option `--year=YYYY` must exist and be a number"
            )
        if (not isdigit(options['id'])) and options['id'] is not None:
            raise CommandError("Option `--id=X` must be a number")
    
    def create_reports(self, year, departamentos=None):
        # Pasamos de una lista de ids de departamento a una lista de departamentos
        if departamentos is None:
            departamentos = GrupoinvestDepartamento.objects.all()
        else:
            departamentos = GrupoinvestDepartamento.objects.filter(id__in=departamentos)

        # Creamos un informe por cada departamento
        for departamento in departamentos:
            self.create_report(year, departamento)

    def create_report(self, year, departamento):
        (investigadores, articulos,
         libros, capitulosLibro, congresos, proyectos,
         convenios, tesis) = self.getData(year, departamento)
        informe = Informe_pdf(year, departamento, investigadores,
                              articulos, libros, capitulosLibro,
                              congresos, proyectos, convenios, tesis)
        informe.go()

    def getData(self, year, departamento):
        #departamento = GrupoinvestDepartamento.objects.get(id=deptID)
        investigadores, usuarios = self.getInvestigadores(year, departamento.id)
        articulos = Publicacion.objects.byUsuariosYearTipo(
            usuarios, year, 'Artículo'
        )
        libros = Publicacion.objects.byUsuariosYearTipo(
            usuarios, year, 'Libro'
        )
        capitulosLibro = Publicacion.objects.byUsuariosYearTipo(
            usuarios, year, 'Capítulo de Libro'
        )
        congresos = Congreso.objects.byUsuariosYear(usuarios, year)
        proyectos = Proyecto.objects.byUsuariosYear(usuarios, year)
        convenios = Convenio.objects.byUsuariosYear(usuarios, year)
        tesis = TesisDoctoral.objects.byUsuariosYear(usuarios, year)
        return (investigadores, articulos,
                libros, capitulosLibro, congresos, proyectos,
                convenios, tesis)

    def getInvestigadores(self, year, deptID):
        fechaInicioMax = datetime.date(year, 12, 31)
        fechaFinMin = datetime.date(year, 1, 1)
        investigadores = GrupoinvestInvestigador.objects.filter(
            departamento__id=deptID
        ).filter(
            Q(fecha_inicio__isnull=False) &
            Q(fecha_inicio__lte=fechaInicioMax)
        ).filter(
            Q(cese__isnull=True) | Q(cese__gte=fechaFinMin)
        ).order_by('apellido1', 'apellido2')

        lista_dni = [investigador.nif for investigador in investigadores]
        usuarios = Usuario.objects.filter(documento__in=lista_dni)
        return investigadores, usuarios
