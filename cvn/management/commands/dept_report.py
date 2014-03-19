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
        dept = [int(options['id'])] if type(options['id']) is str else None
        self.createReports(year, dept)

    def checkArgs(self, options):
        if not isdigit(options['year']):
            raise CommandError(
                "Option `--year=YYYY` must exist and be a number"
            )
        if (not isdigit(options['id'])) and options['id'] is not None:
            raise CommandError("Option `--id=X` must be a number")

    def createReports(self, year, dept=None):
        if dept is None:
            departamentos = GrupoinvestDepartamento.objects.all()
        else:
            departamentos = GrupoinvestDepartamento.objects.filter(
                id__in=dept
            )

        for departamento in departamentos:
            self.createReport(year, departamento)

    def createReport(self, year, departamento):
        (investigadores, articulos,
         libros, capitulosLibro, congresos, proyectos,
         convenios, tesis) = self.getData(year, departamento)
        informe = Informe_pdf(year, departamento, investigadores,
                              articulos, libros, capitulosLibro,
                              congresos, proyectos, convenios, tesis)
        informe.go()

    def getData(self, year, departamento):
        investigadores, usuarios = self.getInvestigadores(
            year, departamento.id
        )
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
        if deptID != 2:
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
        else:
            invesRRHH = [18705, 19484, 18732, 18298, 18588, 19541, 19528,
                         29739, 18590, 17797, 18665, 18719, 19847, 19416,
                         18661, 18668, 18430, 31591, 17872, 19403, 18709,
                         19981, 18463, 29146, 25620, 19010, 18368, 19522,
                         18762, 18228, 19875, 18959, 18712, 19712, 18845,
                         17857, 19000, 18016, 18260, 24224, 19633, 19339,
                         18215, 17811, 19543, 18080, 19563, 31820]
            investigadores = GrupoinvestInvestigador.objects.filter(
                cod_persona__in=invesRRHH
            )

        lista_dni = [investigador.nif for investigador in investigadores]
        usuarios = Usuario.objects.filter(documento__in=lista_dni)
        return investigadores, usuarios
