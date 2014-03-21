# -*- encoding: UTF-8 -*-

from GrupoInvest.models import RRHH
from datetime import datetime
from django.core.management.base import BaseCommand
import csv
import settings
import time


class Command(BaseCommand):
    help = u'Actualiza la referencia del Departamento en los registros \
            de la tabla Investigador'

    # Constructor no es necesario en principio
    def __init__(self):
        super(Command, self).__init__()

    def datetime_convert(self, time_string):
    #Devuelve una cadena en formato datetime inteligible por django.
        if (len(time_string) != 0):
                strp_time = time.strptime(time_string, "%d/%m/%Y %H:%M:%S")
                date_django = datetime.fromtimestamp(time.mktime(strp_time))
                return date_django
        return None

    def date_convert(self, time_string):
    #Devuelve una cadena en formato date inteligible por django.
        if (len(time_string) != 0):
            date_django = datetime.strptime(time_string, '%d/%m/%Y')\
                                  .strftime('%Y-%m-%d')
            return date_django
        return None

    def datetime_to_date(self, date_string):
    # Convierte una cadena datetime en una cadena date
        if (len(date_string) != 0):
            date_string = date_string[:10]
            return self.date_convert(date_string)
        return None

    def string_to_int(self, int_string):
    # Para aquellos campos del modelo que estan definidos como Integer,
    # puede que en el CSV el valor venga vacío, en esos casos devolvemos un 0.
        return int_string if(len(int_string) != 0) else '0'

    def handle(self, *args, **options):
        # Full path and name to your csv file
        dataReader = csv.reader(open(settings.CSV_RRHH_FILE), delimiter='|')
        for row in dataReader:
            # Ignore the header row, import everything else
            if row[0] != 'COD_PERSONA':
                rrhh = RRHH()
                rrhh.cod_persona = row[0]
                rrhh.pas_sn = row[1]
                rrhh.nif = row[2]
                rrhh.id_tipo_documento = row[3]
                rrhh.nombre = row[4]
                rrhh.apellido1 = row[5]
                rrhh.apellido2 = row[6]
                rrhh.sexo = row[7]
                rrhh.f_nacimiento = self.date_convert(row[8])
                rrhh.cod_nacionalidad = self.string_to_int(row[9])
                rrhh.nacionalidad = row[10]
                rrhh.cod_pais_nac = self.string_to_int(row[11])
                rrhh.pais_nac = row[12]
                rrhh.cod_prov_nac = self.string_to_int(row[13])
                rrhh.prov_nac = row[14]
                rrhh.cod_loc_nac = self.string_to_int(row[15])
                rrhh.localidad_nac = row[16]
                rrhh.telefono = row[17]
                rrhh.correo_electronico = row[18]
                rrhh.cod_tipo_via = self.string_to_int(row[19])
                rrhh.via = row[20]
                rrhh.des_direccion = row[21]
                rrhh.cod_postal = row[22]
                rrhh.cod_localidad = self.string_to_int(row[23])
                rrhh.localidad = row[24]
                rrhh.cod_provincia = self.string_to_int(row[25])
                rrhh.prov = row[26]
                rrhh.id_pais = self.string_to_int(row[27])
                rrhh.pais = row[28]
                rrhh.f_desde = self.date_convert(row[29])
                rrhh.f_hasta = self.datetime_to_date(row[30])
                rrhh.cod_cce = self.string_to_int(row[31])
                rrhh.categoria = row[32]
                rrhh.rol = row[33]
                rrhh.cod_departamento = self.string_to_int(row[34])
                rrhh.departamento = row[35]
                rrhh.cod_area = row[36]
                rrhh.area = row[37]
                rrhh.cod_dedicacion = self.string_to_int(row[38])
                rrhh.dedicacion = row[39]
                rrhh.cod_unidad = self.string_to_int(row[40])
                rrhh.unidad = row[41]
                rrhh.cod_subunidad = self.string_to_int(row[42])
                rrhh.subunidad = row[43]
                rrhh.cod_area_esp = row[44]
                rrhh.area_esp = row[45]
                rrhh.cod_departamento_esp = self.string_to_int(row[46])
                rrhh.departamento_esp = row[47]
                rrhh.cod_unidad_esp = self.string_to_int(row[48])
                rrhh.unidad_esp = row[49]
                rrhh.cod_subunidad_esp = self.string_to_int(row[50])
                rrhh.subunidad_esp = row[51]
                rrhh.f_modif_datos_per = self.datetime_convert(row[52])
                rrhh.f_modif_nif = self.datetime_convert(row[53])
                rrhh.f_modif_domicilio = self.datetime_convert(row[54])
                rrhh.f_modif_vig_emp_plaza = self.datetime_convert(row[55])
                rrhh.f_modif_emp_plaza = self.datetime_convert(row[56])
                rrhh.modif_plaza = self.datetime_convert(row[57])
                rrhh.modif_docente = self.datetime_convert(row[58])
                rrhh.modif_pas = self.datetime_convert(row[59])
                rrhh.modif_otro_personal = self.datetime_convert(row[60])
                rrhh.save()
