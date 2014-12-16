# -*- encoding: UTF-8 -*-

from core.models import UserProfile
from core.ws_utils import CachedWS as ws
from cvn import settings as st_cvn
from django.conf import settings as st
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import resolve
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django_tables2 import RequestConfig
from models import Department, ProfessionalCategory, Area
from statistics import settings as st_stats
from tables import DepartmentTable, AreaTable, UnitDetailTable


@login_required
@staff_member_required
def unit_stats(request):
    context = dict()
    context['current_url'] = resolve(request.path_info).url_name
    if context['current_url'] == 'dept_stats':
        context['unit'] = u'Departamentos'
        context['unitStats'] = DepartmentTable(Department.objects.all())
    elif context['current_url'] == 'area_stats':
        context['unit'] = u'Áreas'
        context['unitStats'] = AreaTable(Area.objects.all())
    else:
        raise Http404
    RequestConfig(request, paginate=False).configure(
        context['unitStats'])
    context['validPercentCVN'] = st_stats.PERCENT_VALID_DEPT_CVN
    return render(request, 'statistics/statistics.html', context)


@login_required
@staff_member_required
def unit_stats_detail(request, codigo):
    context = dict()
    current_unit = resolve(request.path_info).url_name
    if current_unit == 'dept_stats_detail':
        context['unit'] = u'Departamentos'
        context['current_url'] = 'dept_stats'
        data_unit = ws.get(st.WS_DEPARTMENTS_AND_MEMBERS_UNIT % codigo)
    elif current_unit == 'area_stats_detail':
        context['unit'] = u'Áreas'
        context['current_url'] = 'area_stats'
        data_unit = ws.get(st.WS_AREAS_AND_MEMBERS_UNIT % codigo)
    else:
        raise Http404

    if data_unit is None:
        raise Http404

    data_unit = data_unit.pop()
    context['validPercentCVN'] = st_stats.PERCENT_VALID_DEPT_CVN
    context['unidad'] = unicode(
        data_unit['unidad']['nombre'])
    context['nombre_corto'] = unicode(
        data_unit['unidad']['nombre_corto'])
    members_list = []
    for member in data_unit['miembros']:
        data = {}
        category = ProfessionalCategory.objects.get(code=member['cod_cce'])
        data['categoria'] = category.name
        data['obligatorio'] = _(u'No')
        if category.is_cvn_required is True:
            data['obligatorio'] = _(u'Sí')
        try:
            user_profile = UserProfile.objects.get(
                rrhh_code=member['cod_persona'])
            data['is_CVN_valid'] = True
            data['CVNStatus'] = _(u'Válido')
            if user_profile.cvn.status != st_cvn.CVNStatus.UPDATED:
                data['is_CVN_valid'] = False
                data['CVNStatus'] = _(u'Inválido')
        except ObjectDoesNotExist:
            data['is_CVN_valid'] = False
            data['CVNStatus'] = _(u'No dispone de CVN')
        data['miembro'] = (member['cod_persona__apellido1'] + ' ' +
                           member['cod_persona__apellido2'] + ', ' +
                           member['cod_persona__nombre'])
        members_list.append(data)
    context['members_list'] = UnitDetailTable(members_list)
    data_table = {1: {'th': {'width': '20%'}}, 2: {'th': {'width': '20%'}},
                  3: {'th': {'width': '20%'}}, 4: {'th': {'width': '20%'}}}

    if current_unit == 'dept_stats_detail':
        context['info_unit'] = DepartmentTable(
            data=Department.objects.filter(code=codigo),
            orderable=False,
            columns=data_table)
    elif current_unit == 'area_stats_detail':
        context['info_unit'] = AreaTable(
            data=Area.objects.filter(code=codigo),
            orderable=False,
            columns=data_table)
    else:
        raise Http404

    RequestConfig(request, paginate=False).configure(
        context['members_list'])
    return render(request, 'statistics/stats_detail.html', context)
