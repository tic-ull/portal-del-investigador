# -*- encoding: UTF-8 -*-

from core.models import UserProfile
from core.utils import wsget
from cvn import settings as stCVN
from django.conf import settings as st
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django_tables2 import RequestConfig
from statistics import settings as stSt
from statistics.models import Department, ProfessionalCategory
from statistics.tables import DepartmentTable, DepartmentDetailTable


@login_required
@staff_member_required
def dept_stats(request):
    context = {}
    context['departmentStats'] = DepartmentTable(Department.objects.all())
    RequestConfig(request, paginate=False).configure(
        context['departmentStats'])
    context['validPercentCVN'] = stSt.PERCENT_VALID_DEPT_CVN
    return render(request, 'statistics/statistics.html', context)


def dept_stats_detail(request, codigo):
    context = {}
    context['validPercentCVN'] = stSt.PERCENT_VALID_DEPT_CVN
    dataDepartment = wsget(st.WS_DEPARTMENT % codigo)
    if dataDepartment is None:
        context['members_list'] = DepartmentDetailTable({})
        context['info_department'] = DepartmentTable({})
        return render(request, 'statistics/stats_detail.html', context)
    context['departamento'] = dataDepartment['departamento']['nombre']
    context['dept_nombre_corto'] =\
        dataDepartment['departamento']['nombre_corto']
    members_list = []
    for member in dataDepartment['miembros']:
        data = {}
        category = ProfessionalCategory.objects.get(code=member['cod_cce'])
        data['categoria'] = category.name
        data['obligatorio'] = _(u'No')
        if category.is_cvn_required is True:
            data['obligatorio'] = _(u'Sí')
        user_data = wsget(st.WS_INFO_PDI % member['cod_persona'])
        try:
            user_profile = UserProfile.objects.get(
                rrhh_code=member['cod_persona'])
            data['is_CVN_valid'] = True
            data['CVNStatus'] = _(u'Válido')
            if user_profile.cvn.status != stCVN.CVNStatus.UPDATED:
                data['is_CVN_valid'] = False
                data['CVNStatus'] = _(u'Inválido')
        except ObjectDoesNotExist:
            data['is_CVN_valid'] = False
            data['CVNStatus'] = _(u'No dispone de CVN')
        data['miembro'] = (user_data['apellido1'] + ' ' +
                           user_data['apellido2'] + ', ' +
                           user_data['nombre'])
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
