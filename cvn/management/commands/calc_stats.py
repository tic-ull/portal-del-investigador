# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import UserProfile
from django.conf import settings as st
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
#import json
import logging
#import urllib

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        department_stats = []
        #WS = '%sget_departamentos_y_miembros' % (st.WS_SERVER_URL)
        #department_list = json.loads(urllib.urlopen(WS).read())
        department_list = [{"departamento": {"nombre": "ANATOMIA, ANAT. PATOL\u00d3GICA E HISTOLOG\u00cdA", "cod_departamento": 98919, "nombre_corto": "AN.PAT.HIS"},
                            "members": [19591, 19729, 26778, 25758, 18721, 18722, 18951, 18857, 27179, 35507, 19381, 27321, 26165, 36086, 35526, 19911, 34888, 20170,
                            35406, 17622, 17883, 18780, 19686, 18577, 19440, 20084, 20214]}, {"departamento": {"nombre": "AN\u00c1LISIS ECON\u00d3MICO", "cod_departamento": 98976, "nombre_corto": "ANA.ECON."},
                            "members": [19168, 19088, 18491, 17552, 19397, 18431, 21439, 18282, 17835, 26188, 17966, 18320, 19282, 18451, 17525, 18358, 19096, 19385, 19163, 18094]},
                            {"departamento": {"nombre": "AN\u00c1LISIS MATEM\u00c1TICO", "cod_departamento": 98918, "nombre_corto": "ANA.MATE."},
                            "members": [19712, 17797, 19339, 19522, 18959, 18705, 17811, 25620, 18709, 18712, 18588, 18845, 18590, 18719, 18080, 19875, 18215, 19484, 29739, 19633, 18228, 19000, 18463, 18368,
                            24224, 19010, 19528, 18762, 19403, 31820, 19981, 17872, 18260, 19541, 19543, 29146, 18016, 18661, 18665, 19563, 18668, 18298, 18430]}]
        for department in department_list:
            data = {}
            data['departamento'] = department['departamento']['nombre']
            data['num_members'] = len(department['members'])
            data.update(self.calc_stats_department(department['members']))
            department_stats.append(data)
        print department_stats

    def calc_stats_department(self, members_list):
        dict_department = {}
        num_cvn_update = 0
        for member in members_list:
            try:
                user = UserProfile.objects.get(rrhh_code=member)
                if stCVN.CVN_STATUS[user.cvn.status][0] == 0:
                    num_cvn_update += 1
            except ObjectDoesNotExist:
                pass
        dict_department['num_cvn_update'] = num_cvn_update
        dict_department['cvn_percent_updated'] = ((num_cvn_update * 100.0) /
                                                  len(members_list))
        return dict_department
