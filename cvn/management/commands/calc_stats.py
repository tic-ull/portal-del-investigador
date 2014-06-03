# -*- encoding: UTF-8 -*-

#from cvn import settings as stCVN
from cvn.utils import calc_stats_department
from django.conf import settings as st
from django.core.management.base import BaseCommand
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
            data['departamento'] = department['departamento']['nombre']
            data.update(calc_stats_department(department['miembros']))
            department_stats.append(data)
        # Update data shared in memory
        print department_stats
