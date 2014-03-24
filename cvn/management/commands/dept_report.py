# -*- encoding: UTF-8 -*-

from cvn.models import (Publicacion, Congreso, Proyecto, Convenio,
                        TesisDoctoral, Usuario)
from cvn.utils import isdigit
from django.conf import settings as st
from django.core.management.base import BaseCommand, CommandError
from informe_pdf import Informe_pdf
from optparse import make_option
from viinvDB.models import GrupoinvestDepartamento, GrupoinvestInvestigador
import urllib


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
        print 'Generando PDF para %s ... ' % (departamento.nombre)
        if investigadores:
            informe = Informe_pdf(year, departamento, investigadores,
                                  articulos, libros, capitulosLibro,
                                  congresos, proyectos, convenios, tesis)
            informe.go()
            print 'OK\n'
        else:
            print 'ERROR: No hay Investigadores\n'

    def getData(self, year, departamento):
        investigadores, usuarios = self.getInvestigadores(
            year, departamento
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

    def getInvestigadores(self, year, dept):
        WS = '%sodin/core/rest/get_pdi_vigente?' \
             'cod_departamento=%s&ano=%s' % (st.WS_SERVER_URL,
                                             dept.codigo,
                                             year)
        invesRRHH = urllib.urlopen(WS).read()
        invesRRHH = invesRRHH.replace('[', '').replace(']', '').split(', ')
        investigadores = GrupoinvestInvestigador.objects.filter(
            cod_persona__in=invesRRHH
        ).order_by('apellido1', 'apellido2')

        lista_dni = [investigador.nif for investigador in investigadores]
        usuarios = Usuario.objects.filter(documento__in=lista_dni)
        return investigadores, usuarios
