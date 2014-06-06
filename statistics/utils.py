# -*- encondig: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
# PROFESSIONAL CATEGORY
from statistics.settings import PROFESSIONAL_CATEGORY
from django.conf import settings as st
import json
import urllib


def calc_stats_department(members_list):
    dict_department = {}
    num_cvn_update = 0
    num_computable_members = 0
    for member in members_list:
        try:
            user = UserProfile.objects.get(rrhh_code=member)
            WS = '%sget_info_pdi?cod_persona=%s' % (st.WS_SERVER_URL, member)
            info_pdi = json.loads(urllib.urlopen(WS).read())
            if (info_pdi['cod_categoria'] in PROFESSIONAL_CATEGORY):
                num_computable_members += 1
                if user.cvn.status == stCVN.CVNStatus.UPDATED:
                    num_cvn_update += 1
        except ObjectDoesNotExist:
            pass
    dict_department['num_computable_members'] = num_computable_members
    dict_department['num_cvn_update'] = num_cvn_update
    try:
        dict_department['cvn_percent_updated'] = ((num_cvn_update * 100.0) /
                                                  num_computable_members)
    except ZeroDivisionError:  # Departments with zero computable members
        dict_department['cvn_percent_updated'] = 100
    return dict_department
