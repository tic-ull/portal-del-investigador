# -*- encoding: UTF-8 -*-

from core.tables import Table
from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables

EURO_TEMPLATE = '''
    {% if value != None %}
        {{ value|floatformat:2 }} &euro;
    {% endif %}
'''


class SummaryYearTable(Table):

    ejercicio = tables.Column(
        accessor='ejercicio',
        verbose_name=_(u'Ejercicio'),
        attrs={'td': {'align': 'left'}})

    inicial = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='inicial',
        verbose_name=_(u'Inicial'),
        orderable=False)

    reserva = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='reserva',
        verbose_name=_(u'Reserva de Crédito'),
        orderable=False)

    orgSaldoRC = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='orgSaldoRC',
        verbose_name=_(u'Saldo RC'),
        orderable=False)

    orgSaldoA = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='orgSaldoA',
        verbose_name=_(u'Saldo A'),
        orderable=False)

    orgSaldoD = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='orgSaldoD',
        verbose_name=_(u'Saldo D'),
        orderable=False)

    orgModificaciones = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='orgModificaciones',
        verbose_name=_(u'Modificaciones'),
        orderable=False)

    orgTotalObligaciones = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='orgTotalObligaciones',
        verbose_name=_(u'Total Obligaciones'),
        orderable=False)

    orgSaldoDisponible = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='orgSaldoDisponible',
        verbose_name=_(u'Saldo disponible'),
        orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed',
                 'style': 'text-align: right;'}


class TotalSummaryYearTable(Table):

    orgTotalObligaciones = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='orgTotalObligaciones',
        verbose_name=_(u'Total Obligaciones'))

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}
        orderable = False


class SummaryConceptTable(Table):

    concepto = tables.Column(
        accessor='concepto',
        verbose_name=_(u'Concepto'),
        attrs={'td': {'align': 'left'}})

    funSaldoEXP = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='funSaldoEXP',
        verbose_name=_(u'Saldo EXP'),
        orderable=False)

    funSaldoFAC = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='funSaldoFAC',
        verbose_name=_(u'Saldo Facturas'),
        orderable=False)

    funSaldoA = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='funSaldoA',
        verbose_name=_(u'Saldo A'),
        orderable=False)

    funSaldoD = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='funSaldoD',
        verbose_name=_(u'Saldo D'),
        orderable=False)

    funTotalObligaciones = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='funTotalObligaciones',
        verbose_name=_(u'Total Obligaciones'),
        orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed',
                 'style': 'text-align: right;'}


class BreakdownYearTable(SummaryConceptTable):

    ejercicio = tables.Column(
        accessor='ejercicio',
        verbose_name=_(u'Ejercicio'),
        attrs={'td': {'align': 'left'}})

    concepto = tables.Column(
        accessor='concepto',
        verbose_name=_(u'Concepto'),
        orderable=False,
        attrs={'td': {'align': 'left'}})

    class Meta:
        attrs = {'class': 'table table-striped table-condensed',
                 'style': 'text-align: right;'}
        fields = ('ejercicio', )


class TotalConceptAndBreakdownTable(Table):

    funSaldoEXP = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='funSaldoEXP',
        verbose_name=_(u'Saldo total EXP'),
        orderable=False)

    funSaldoFAC = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='funSaldoFAC',
        verbose_name=_(u'Saldo total Facturas'),
        orderable=False)

    funSaldoA = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='funSaldoA',
        verbose_name=_(u'Saldo total A'),
        orderable=False)

    funSaldoD = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='funSaldoD',
        verbose_name=_(u'Saldo total D'),
        orderable=False)

    funTotalObligaciones = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='funTotalObligaciones',
        verbose_name=_(u'Total Obligaciones'),
        orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}


class DetailTable(Table):

    ejercicio = tables.Column(
        accessor='ejercicio',
        verbose_name=_(u'Ejercicio'),
        orderable=False)

    numero = tables.Column(
        accessor='numero',
        verbose_name=_(u'Número'))

    tipo = tables.Column(
        accessor='tipo',
        verbose_name=_(u'Tipo'),
        orderable=False)

    proveedor = tables.Column(
        accessor='proveedor',
        verbose_name=_(u'Proveedor'),
        orderable=False)

    descripcion = tables.Column(
        accessor='descripcion',
        verbose_name=_(u'Descripción'),
        orderable=False)

    concepto = tables.Column(
        accessor='concepto',
        verbose_name=_(u'Concepto'),
        orderable=False)

    variaciones = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='variaciones',
        verbose_name=_(u'Variaciones'),
        orderable=False,
        attrs={'td': {'align': 'right'}})

    gastos = tables.TemplateColumn(
        EURO_TEMPLATE,
        accessor='gastos',
        verbose_name=_(u'Gastos'),
        orderable=False,
        attrs={'td': {'align': 'right'}})

    asiento = tables.Column(
        accessor='asiento',
        verbose_name=_(u'Asiento'),
        orderable=False)

    validacion = tables.Column(
        accessor='validacion',
        verbose_name=_(u'Validación'),
        orderable=False)

    pago = tables.Column(
        accessor='pago',
        verbose_name=_(u'Pago'),
        orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed',
                 'style': 'text-align: left;'}


URL_TEMPLATE = '''
    <a href='{% url 'accounting_detail' record.CODIGO %}'>{{ record.NAME }}</a>
'''

DATE_TEMPLATE = '''
    {{ record.DATE|date:'d-m-Y' }}
'''


class AccountingTableProjects(Table):

    codigo_proyecto = tables.Column(
        accessor='CODIGO',
        verbose_name=_(u'Código'))

    nombre_proyecto = tables.TemplateColumn(
        URL_TEMPLATE,
        accessor='NAME',
        verbose_name=_(u'Nombre'),
        attrs={'th': {'width': '40%'}})

    ip_proyecto = tables.Column(
        accessor='IP',
        verbose_name=_(u'IP'),
        attrs={'th': {'width': '25%'}})

    fecha_inicio_proyecto = tables.TemplateColumn(
        DATE_TEMPLATE,
        accessor='DATE.date',
        verbose_name=_(u'Fecha Aceptación'))

    clave_contable_proyecto = tables.Column(
        accessor='CONT_KEY',
        verbose_name=_(u'Clave contable'))

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}


class AccountingTableAgreements(Table):

    codigo_convenio = tables.Column(
        accessor='CODIGO',
        verbose_name=_(u'Código'))

    nombre_convenio = tables.TemplateColumn(
        URL_TEMPLATE,
        accessor='NAME',
        verbose_name=_(u'Nombre'),
        attrs={'th': {'width': '40%'}})

    ip_convenio = tables.Column(
        accessor='IP',
        verbose_name=_(u'IP'),
        attrs={'th': {'width': '25%'}})

    fecha_inicio_convenio = tables.TemplateColumn(
        DATE_TEMPLATE,
        accessor='DATE.date',
        verbose_name=_(u'Fecha Inicio'))

    clave_contable_convenio = tables.Column(
        accessor='CONT_KEY',
        verbose_name=_(u'Clave contable'))

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}
