# -*- encoding: UTF-8 -*-

#from django.conf import settings as st
from django.conf import settings as st
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from statistics.settings import PERCENT_VALID_DEPT_CVN
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
        departmentStats.append(data)
    #
    context['departmentStats'] = departmentStats
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
