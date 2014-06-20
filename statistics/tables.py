# -*- encoding: UTF-8 -*-

import django_tables2 as tables

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
NAME_TEMPLATE = '''
<a href='{% url 'stats_detail' record.code %}'>{{ record.name }}</a>
'''


class DepartmentTable(tables.Table):
    name = tables.TemplateColumn(NAME_TEMPLATE, attrs={'th': {'width': '38%'}})
    num_valid_cvn = tables.Column(accessor='number_valid_cvn',
                                  attrs={'th': {'width': '14%'}})
    computable_member = tables.Column(accessor='computable_members',
                                      attrs={'th': {'width': '11%'}})
    total_member = tables.Column(accessor='total_members',
                                 attrs={'th': {'width': '11%'}})
    percentage = tables.TemplateColumn(PERCENTAGE_TEMPLATE)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}
        ordered = {'name'}
