# -*- encoding: UTF-8 -*-

from cvn.models import Publicacion, Congreso, Proyecto, Convenio, TesisDoctoral, Usuario
from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
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
            raise CommandError("Option `--year=YYYY` must exist and be a number.")
        else:
            self.year = int(options['year'])
        
        if not checkDigit(options['id']):
            raise CommandError("Option `--id=X` must exist and be a number.")
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
        #dataDept = Get_datos_departamento(self.deptID, self.year)
        investigadores, usuarios = self.query_investigadores(self.deptID)
        #usuarios = dataDept.get_usuarios()
        departamento = GrupoinvestDepartamento.objects.get(id=self.deptID)
        #investigadores = dataDept.get_investigadores()
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

    def query_investigadores(self, identificador, tipo="departamento"):
        assert (tipo == "departamento" or tipo == "instituto")
        fecha_inicio_max = datetime.date(self.year, 12, 31)
        fecha_fin_min = datetime.date(self.year, 1, 1)
        investigadores = None
        if tipo == "departamento":
            investigadores = GrupoinvestInvestigador.objects.filter(departamento__id=identificador)
        else:
            investigadores = GrupoinvestInvestigador.objects.filter(instituto__id=identificador)
        
        investigadores = investigadores.filter(Q(fecha_inicio__isnull=False)&Q(fecha_inicio__lte=fecha_inicio_max))
        investigadores = investigadores.filter(Q(cese__isnull=True)|Q(cese__gte=fecha_fin_min))
        investigadores = investigadores.order_by('apellido1', 'apellido2')
        
        lista_dni = [investigador.nif for investigador in investigadores]
        # Guardamos los objectos Usuario, de los investigadores GrupoinvestInvestigador
        # Se extraen de esta manera por estar en bbdd diferentes
        usuarios = Usuario.objects.filter(documento__in=lista_dni)
        return investigadores, usuarios
