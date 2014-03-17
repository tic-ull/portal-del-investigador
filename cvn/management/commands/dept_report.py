# -*- encoding: UTF-8 -*-

from cvn.models import (Publicacion, Congreso, Proyecto, Convenio,
                        TesisDoctoral, Usuario)
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from informe_pdf import Informe_pdf
from optparse import make_option
from viinvDB.models import GrupoinvestDepartamento, GrupoinvestInvestigador
import datetime


def checkDigit(obj):
    if obj is None or not obj.isdigit():
        return False
    else:
        return True


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
        if not checkDigit(options['year']):
            raise CommandError(
                "Option `--year=YYYY` must exist and be a number"
            )
        else:
            self.year = int(options['year'])
        if not checkDigit(options['id']):
            raise CommandError("Option `--id=X` must exist and be a number")
        else:
            self.deptID = int(options['id'])

    def create_report(self):
        (departamento, investigadores, articulos,
         libros, capitulosLibro, congresos, proyectos,
         convenios, tesis) = self.getData()
        informe = Informe_pdf(self.year, departamento, investigadores,
                              articulos, libros, capitulosLibro,
                              congresos, proyectos, convenios, tesis)
        informe.go()

    def getData(self):
        departamento = GrupoinvestDepartamento.objects.get(id=self.deptID)
        investigadores, usuarios = self.getInvestigadores()
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
        proyectos = Proyecto.objects.byUsuariosYear(usuarios, self.year)
        convenios = Convenio.objects.byUsuariosYear(usuarios, self.year)
        tesis = TesisDoctoral.objects.byUsuariosYear(usuarios, self.year)
        return (departamento, investigadores, articulos,
                libros, capitulosLibro, congresos, proyectos,
                convenios, tesis)

    def getInvestigadores(self):
        fechaInicioMax = datetime.date(self.year, 12, 31)
        fechaFinMin = datetime.date(self.year, 1, 1)
        investigadores = GrupoinvestInvestigador.objects.filter(
            departamento__id=self.deptID
        ).filter(
            Q(fecha_inicio__isnull=False) &
            Q(fecha_inicio__lte=fechaInicioMax)
        ).filter(
            Q(cese__isnull=True) | Q(cese__gte=fechaFinMin)
        ).order_by('apellido1', 'apellido2')

        lista_dni = [investigador.nif for investigador in investigadores]
        usuarios = Usuario.objects.filter(documento__in=lista_dni)
        return investigadores, usuarios
