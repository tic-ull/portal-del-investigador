# -*- encoding: UTF-8 -*-

#from django.conf import settings as st
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from statistics.settings import PERCENT_VALID_DEPT_CVN
#import json
#import urllib


@ login_required
@staff_member_required
def statistics(request):
    # Access to data in memory, cache...
    context = {}
    departmentStats = [{'numCVNupdate': 0,
                        'cvnPercentUpdated': 0,
                        'numMembers': 27,
                        'departamento': u'ANATOMIA, ANAT.\
                        PATOLÓGICA E HISTOLOGÍA'},
                       {'numCVNupdate': 0,
                        'cvnPercentUpdated': 80,
                        'numMembers': 20,
                        'departamento': 'ANÁLISIS ECONÓMICO'},
                       {'numCVNupdate': 15,
                        'cvnPercentUpdated': 71,
                        'numMembers': 20,
                        'departamento': 'BECARIOS'},
                       {'numCVNupdate': 15,
                        'cvnPercentUpdated': 71,
                        'numMembers': 20,
                        'departamento': 'DEPT1'},
                       {'numCVNupdate': 15,
                        'cvnPercentUpdated': 91,
                        'numMembers': 27,
                        'departamento': 'DEPT2'},
                       {'numCVNupdate': 35,
                        'cvnPercentUpdated': 75,
                        'numMembers': 89,
                        'departamento': 'DEPT3'},
                       {'numCVNupdate': 0,
                        'cvnPercentUpdated': 100,
                        'numMembers': 43,
                        'departamento': 'ANÁLISIS MATEMÁTICO'}]
    # Paginator- Show X department per page
    paginator = Paginator(departmentStats, 5)
    page = request.GET.get('page')
    try:
        department_list = paginator.page(page)
    except PageNotAnInteger:
        department_list = paginator.page(1)
    except EmptyPage:
        department_list = paginator.page(paginator.num_pages)
    context['departmentStats'] = department_list
    context['validPercentCVN'] = PERCENT_VALID_DEPT_CVN
    return render(request, 'statistics/statistics.html', context)
