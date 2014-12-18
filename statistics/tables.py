# -*- encoding: UTF-8 -*-

from core.tables import Table
from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables


class UnitTable(Table):

    PERCENTAGE_TEMPLATE = '''
        {% load l10n %}

        <div class="progress">
            <div class="progress-bar
                {% if record.percentage >= validPercentCVN %}
                    progress-bar-success
                {% else %}
                    progress-bar-danger
                {% endif %}"
                role="progressbar" aria-valuenow={{ record.percentage }}
                aria-valuemin="0" aria-valuemax="100"
                style="width: {{ record.percentage|unlocalize }}%">
                    <span class="num_pcnt">
                        {{ record.percentage|floatformat:1 }}%
                    </span>
            </div>
        </div>
    '''

    NAME_TEMPLATE = ''' record.name '''

    name = tables.TemplateColumn(NAME_TEMPLATE, attrs={'th': {'width': '38%'}})

    valid_cvn = tables.Column(
        accessor='number_valid_cvn',
        attrs={'th': {'width': '15%'},
               'data_helper': _('CVN actualizado y con NIF/NIE correcto')})

    computable_member = tables.Column(accessor='computable_members',
                                      attrs={'th': {'width': '14%'}})

    total_member = tables.Column(accessor='total_members',
                                 attrs={'th': {'width': '11%'}})

    percentage = tables.TemplateColumn(
        PERCENTAGE_TEMPLATE,
        attrs={'data_helper': _(u'CVN válidos / Miembros computables')})

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}


class DepartmentTable(UnitTable):

    NAME_TEMPLATE = '''
    <a href='{% url 'dept_stats_detail' record.code %}'>{{ record.name }}</a>
    '''

    name = tables.TemplateColumn(NAME_TEMPLATE, attrs={'th': {'width': '38%'}})

    class Meta(UnitTable.Meta):
        pass


class AreaTable(UnitTable):

    NAME_TEMPLATE = '''
    <a href='{% url 'area_stats_detail' record.code %}'>{{ record.name }}</a>
    '''

    name = tables.TemplateColumn(NAME_TEMPLATE, attrs={'th': {'width': '38%'}})

    class Meta(UnitTable.Meta):
        pass


class UnitDetailTable(Table):
    CVN_STATUS_TEMPLATE = '''
        {% if record.is_CVN_valid %}
            <div style="padding: 4px; text-align:center;"
                 class="alert alert-success">
        {% else %}
            <div style="padding: 4px; text-align:center;"
                 class="alert alert-danger">
        {% endif %}
                {{ record.CVNStatus }}
            </div>
    '''

    research = tables.Column(accessor='miembro',
                             verbose_name=_(u'Investigador'))

    category = tables.Column(accessor='categoria',
                             verbose_name=_(u'Categoría'))

    cvn_required = tables.Column(accessor='obligatorio',
                                 verbose_name=_(u'CVN obligatorio'))

    cvn_status = tables.TemplateColumn(CVN_STATUS_TEMPLATE,
                                       accessor='CVNStatus',
                                       verbose_name=_(u'Estado CVN'),
                                       attrs={'td': {'style': 'padding: 0'}})

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}
