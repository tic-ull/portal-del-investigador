# -*- encoding: UTF-8 -*-

from core.models import UserProfile
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
import json
import urllib


@login_required
@staff_member_required
def statistics(request):
    context = {}
    context['departmentStats'] = DepartmentTable(Department.objects.all())
    RequestConfig(request, paginate=False).configure(
        context['departmentStats'])
    context['validPercentCVN'] = stSt.PERCENT_VALID_DEPT_CVN
    return render(request, 'statistics/statistics.html', context)


def stats_detail(request, codigo):
    context = {}
    try:
        dataDepartment = json.loads(
            urllib.urlopen(st.WS_DEPARTMENT % codigo).read())
        context['departamento'] = dataDepartment['departamento']['nombre']
        members_list = []
        for member in dataDepartment['miembros']:
            data = {}
            member_info = json.loads(
                urllib.urlopen(st.WS_INFO_PDI % member['cod_persona']).read())
            data['miembro'] = (
                member_info['apellido1'] + ' ' +
                member_info['apellido2'] + ', ' +
                member_info['nombre'])
            data['categoria'] = member_info['categoria']
            data['obligatorio'] = _(u'No')
            if ProfessionalCategory.objects.get(code=member_info[
                    'cod_categoria']).is_cvn_required is True:
                data['obligatorio'] = _(u'Sí')
            try:
                user = UserProfile.objects.get(rrhh_code=member['cod_persona'])
                data['CVNStatus'] = _(u'Válido')
                data['is_CVN_valid'] = True
                if user.cvn.status != stCVN.CVNStatus.UPDATED:
                    data['is_CVN_valid'] = False
                    data['CVNStatus'] = _(u'Inválido')
            except ObjectDoesNotExist:
                data['is_CVN_valid'] = False
                data['CVNStatus'] = _(u'No dispone de CVN')
            members_list.append(data)
        context['members_list'] = DepartmentDetailTable(members_list)
    except IOError:
        pass
    RequestConfig(request, paginate=False).configure(
        context['members_list'])
    return render(request, 'statistics/stats_detail.html', context)
