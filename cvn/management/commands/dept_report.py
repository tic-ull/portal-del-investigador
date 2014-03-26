# -*- encoding: UTF-8 -*-

from cvn.models import (Publicacion, Congreso, Proyecto, Convenio,
                        TesisDoctoral, Usuario)
from cvn.utils import isdigit
from django.conf import settings as st
from django.core.management.base import BaseCommand, CommandError
from informe_pdf import Informe_pdf
from optparse import make_option
from viinvDB.models import GrupoinvestDepartamento, GrupoinvestInvestigador
import simplejson as json
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

        invesRRHH = [19712, 17797, 19847, 19339, 19522, 18959, 18705, 17811,
                     25620, 18709, 18712, 18588, 18845, 18590, 18719, 18080,
                     19875, 18215, 19484, 29739, 18732, 19633, 18228, 19000,
                     18463, 18368, 24224, 19010, 19528, 18762, 19403, 31820,
                     19981, 17872, 17857, 18260, 19541, 19543, 19416, 29146,
                     18016, 18661, 18665, 19563, 18668, 18298, 18430]

        #invesRRHH = urllib.urlopen(WS).read()
        #invesRRHH = invesRRHH.replace('[', '').replace(']', '').split(', ')

        inves = list()
        for inv in invesRRHH:
            WS = '%sodin/core/rest/get_info_pdi?cod_persona=%s&ano=%s' % (
                st.WS_SERVER_URL, inv, year)
            dataInv = json.loads(urllib.urlopen(WS).read())
            inves.append(dataInv)
        investigadores = sorted(inves, key=lambda k: "%s %s" % (
            k['apellido1'], k['apellido2']))
        usuarios = Usuario.objects.filter(
            documento__in=GrupoinvestInvestigador.objects.filter(
                cod_persona__in=invesRRHH).values('nif'))
        return investigadores, usuarios
