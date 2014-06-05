# -*- encondig: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist


def calc_stats_department(members_list):
    dict_department = {}
    num_cvn_update = 0
    for member in members_list:
        try:
            user = UserProfile.objects.get(rrhh_code=member)
            if stCVN.CVN_STATUS[user.cvn.status][0] == 0:
                num_cvn_update += 1
        except ObjectDoesNotExist:
            pass
    dict_department['num_members'] = len(members_list)
    dict_department['num_cvn_update'] = num_cvn_update
    try:
        dict_department['cvn_percent_updated'] = ((num_cvn_update * 100.0) /
                                                  len(members_list))
    except ZeroDivisionError:  # Departments with zero members
        dict_department['cvn_percent_updated'] = 0
    return dict_department
