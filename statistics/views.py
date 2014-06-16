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
from statistics.models import Department
import json
import urllib


@ login_required
@staff_member_required
def statistics(request):
    context = {}
    context['departmentStats'] = Department.objects.all().order_by('name')
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
    WS = '%sget_departamento_y_miembros?cod_departamento=%s' %\
        (st.WS_SERVER_URL, codigo)
    try:
        dataDepartment = json.loads(urllib.urlopen(WS).read())
        context['departamento'] = dataDepartment['departamento']['nombre']
        members_list = []
        for member in dataDepartment['miembros']:
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
                data['obligatorio'] = _(u'Sí')
            try:
                user = UserProfile.objects.get(rrhh_code=member['cod_persona'])
                data['CVNStatus'] = _(u'Válido')
                if user.cvn.status == stCVN.CVNStatus.EXPIRED:
                    data['CVNStatus'] = _(u'Inválido')
            except ObjectDoesNotExist:
                data['CVNStatus'] = _(u'No dispone de CVN')
            members_list.append(data)
        context['members_list'] = members_list
    except IOError:
        pass
    return render(request, 'statistics/stats_detail.html', context)
