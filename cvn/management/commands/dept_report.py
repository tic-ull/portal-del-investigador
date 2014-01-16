# -*- encoding: utf8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import connections   # conexión a la BBDD
from get_datos_departamento import Get_datos_departamento
from informe_pdf import Informe_pdf


class Command(BaseCommand):
    help = u'Genera un pdf con los datos de un departamento. \
            Usa una BBDD congelada accesible por SQL'
    """ examples ./manage.py dept_report -y2012 -i6 """
    option_list = BaseCommand.option_list + (
        make_option(
            "-y",
            "--year",
            dest="year",
            help="Specify year.",
        ),
        make_option(
            "-i",
            "--id",
            dest="id",
            help="Specify id of the department.",
        ),
    )

    def __init__(self):
        super(Command, self).__init__()

    def create_DDBB_connection(self):
        """
        Establece la conexión a la BBDD correspondiente a la memoria
        que se quiere generar
        Para cada memoria habrá una BBDD cuyas tablas tienen el
        prefijo memYYYY_ donde YYYY corresponde al año.
        TODO: cambiar los prefijos en la memoria 2012 existente

        Los datos de conexión a la BBDD correspondiente tienen que
        estar en el settings y se irán añadiendo a medida que haya
        """
        self.CONNECTION = connections['mem' + self.YEAR + '_db_alias']

    def handle(self, *args, **options):
        if options['year'] is None:
            raise CommandError("Option `--year=...` must be specified.")
        else:
            self.YEAR = options['year']

        if options['id'] is None:
            raise CommandError("Option `--id=...` must be specified.")
        else:
            self.ID = options['id']
        self.create_DDBB_connection()
        self.create_report()

    def test_lista_investigadores(self):
        test = Get_datos_departamento(self.CONNECTION, 3, 2012)
        investigadores = test.get_investigadores()
        print investigadores
        informe = Informe_pdf(2012, {"nombre": "PSICOLOGÍA SOCIAL COGNITIVA"},
                              investigadores, [], [])
        informe.go()

    def create_report(self):
        data_dept = Get_datos_departamento(self.CONNECTION, self.ID, self.YEAR)
        datos_basicos = data_dept.get_datos_basicos()
        investigadores = data_dept.get_investigadores()
        produccion = data_dept.get_produccion()
        actividad = data_dept.get_actividad()
        informe = Informe_pdf(self.YEAR, datos_basicos, investigadores,
                              produccion, actividad)
        informe.go()
