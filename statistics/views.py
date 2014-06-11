# -*- encoding: UTF-8 -*-

from core.models import UserProfile
from cvn import settings as stCVN
from django.conf import settings as st
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils.translation import ugettext as _
from statistics.settings import PERCENT_VALID_DEPT_CVN, PROFESSIONAL_CATEGORY
from statistics.utils import calc_stats_department
import json
import urllib


@ login_required
@staff_member_required
def statistics(request):
    # Access to data in memory, cache...
    context = {}
    # This part is calculate in admincommand 'calc_stats'
    # and save in shared memory
    departmentStats = []
    WS = '%sget_departamentos_y_miembros' % (st.WS_SERVER_URL)
    department_list = json.loads(urllib.urlopen(WS).read())
    for department in department_list:
        data = {}
        data['nombre'] = department['departamento']['nombre']
        data['nombre_corto'] = department['departamento']['nombre_corto']
        data.update(calc_stats_department(department['miembros']))
        # Codigo departamenteo para mostrar los detalles
        data['codigo'] = department['departamento']['cod_departamento']
        departmentStats.append(data)
    #
#    context['departmentStats'] = departmentStats
    context['departmentStats'] = sorted(departmentStats,
                                        key=lambda departmentStats:
                                        departmentStats['nombre'])
    context['validPercentCVN'] = PERCENT_VALID_DEPT_CVN
    return render(request, 'statistics/statistics.html', context)

    # Paginator- Show X department per page
#    paginator = Paginator(departmentStats, 20)
#    page = request.GET.get('page')
#    try:
#        department_list = paginator.page(page)
#    except PageNotAnInteger:
#        department_list = paginator.page(1)
#    except EmptyPage:
#        department_list = paginator.page(paginator.num_pages)
#    context['departmentStats'] = department_list
#    context['validPercentCVN'] = PERCENT_VALID_DEPT_CVN
#    return render(request, 'statistics/statistics.html', context)


def stats_detail(request, codigo):
    context = {}
    # Buscar datos del departamento (miembros, categoria. etc...)
    # WS = '%sget_info_departamento?cod_departamento=%s' % (st.WS_SERVER_URL,
    # codigo)
    context['departamento'] = u'Departamento Prueba'
    WSlist = [{"cod_persona": 18483, "cod_cce": 6289},
              {"cod_persona": 19507, "cod_cce": 5610},
              {"cod_persona": 19613, "cod_cce": 5612},
              {"cod_persona": 19367, "cod_cce": 5609},
              {"cod_persona": 25629, "cod_cce": 6291},
              {"cod_persona": 18129, "cod_cce": 6643},
              {"cod_persona": 18525, "cod_cce": 6291},
              {"cod_persona": 18919, "cod_cce": 6291},
              {"cod_persona": 18493, "cod_cce": 6291},
              {"cod_persona": 18355, "cod_cce": 6289},
              {"cod_persona": 18970, "cod_cce": 6289},
              {"cod_persona": 19455, "cod_cce": 6291},
              {"cod_persona": 18395, "cod_cce": 5610}]
    members_list = []
    for member in WSlist:
        data = {}
        WS = '%sget_info_pdi?cod_persona= %s' % (st.WS_SERVER_URL,
                                                 member['cod_persona'])
        member_info = json.loads(urllib.urlopen(WS).read())
        data['miembro'] = (member_info['apellido2'] + ' ' +
                           member_info['apellido1'] + ', ' +
                           member_info['nombre'])
        data['categoria'] = member_info['categoria']
        data['obligatorio'] = _(u'No')
        if member_info['cod_categoria'] in PROFESSIONAL_CATEGORY:
            data['obligatorio'] = _(u'Si')
        try:
            user = UserProfile.objects.get(rrhh_code=member['cod_persona'])
            data['CVNStatus'] = stCVN.CVN_STATUS[user.cvn.status][1]
        except ObjectDoesNotExist:
            data['CVNStatus'] = _(u'No dispone de CVN')
        members_list.append(data)
    context['members_list'] = members_list
    return render(request, 'statistics/stats_detail.html', context)
