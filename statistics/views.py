# -*- encoding: UTF-8 -*-

from core.models import UserProfile
from core.redis_utils import wsget
from cvn import settings as st_cvn
from django.conf import settings as st
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django_tables2 import RequestConfig
from models import Department, ProfessionalCategory
from tables import DepartmentTable, DepartmentDetailTable
import settings as st_stat


@login_required
@staff_member_required
def dept_stats(request):
    context = dict()
    context['departmentStats'] = DepartmentTable(Department.objects.all())
    RequestConfig(request, paginate=False).configure(
        context['departmentStats'])
    context['validPercentCVN'] = st_stat.PERCENT_VALID_DEPT_CVN
    return render(request, 'statistics/statistics.html', context)


@login_required
@staff_member_required
def dept_stats_detail(request, codigo):
    context = dict()
    data_department = wsget(st.WS_DEPARTMENT % codigo)
    if data_department is None:
        raise Http404
    context['validPercentCVN'] = st_stat.PERCENT_VALID_DEPT_CVN
    context['departamento'] = unicode(
        data_department['unidad']['nombre'])
    context['dept_nombre_corto'] = unicode(
        data_department['unidad']['nombre_corto'])
    members_list = []
    for member in data_department['miembros']:
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
    context['members_list'] = DepartmentDetailTable(members_list)
    data_table = {1: {'th': {'width': '20%'}}, 2: {'th': {'width': '20%'}},
                  3: {'th': {'width': '20%'}}, 4: {'th': {'width': '20%'}}}
    context['info_department'] = DepartmentTable(
        data=Department.objects.filter(code=codigo),
        orderable=False,
        columns=data_table)
    RequestConfig(request, paginate=False).configure(
        context['members_list'])
    return render(request, 'statistics/stats_detail.html', context)
