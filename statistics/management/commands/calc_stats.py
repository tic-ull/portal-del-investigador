# -*- encoding: UTF-8 -*-

#from cvn import settings as stCVN
from django.conf import settings as st
from django.core.management.base import BaseCommand
from statistics.utils import calc_stats_department
import json
import logging
import urllib

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        department_stats = []
        WS = '%sget_departamentos_y_miembros' % (st.WS_SERVER_URL)
        department_list = json.loads(urllib.urlopen(WS).read())
        for department in department_list:
            data = {}
            data['nombre'] = department['departamento']['nombre']
            data['nombre_corto'] = department['departamento']['nombre_corto']
            data['codigo'] = department['departamento']['cod_departamento']
            data.update(calc_stats_department(department['miembros']))
            department_stats.append(data)
        # Update data shared in memory
        #print department_stats
        return department_stats  # Remove
