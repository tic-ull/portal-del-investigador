# -*- encoding: UTF-8 -*-

from core.tables import Table
from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables

MONEY_TEMPLATE = '''
    {% if value != None %}
        {{ value|floatformat:2 }} &euro;
    {% endif %}
'''


class SummaryYearTable(Table):

    ejercicio = tables.Column(
        accessor='ejercicio',
        verbose_name=_(u'Ejercicio'))

    inicial = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='inicial',
        verbose_name=_(u'Inicial'),
        orderable=False)

    reserva = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='reserva',
        verbose_name=_(u'Reserva de Crédito'),
        orderable=False)

    orgSaldoRC = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='orgSaldoRC',
        verbose_name=_(u'Saldo RC'),
        orderable=False)

    orgSaldoA = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='orgSaldoA',
        verbose_name=_(u'Saldo A'),
        orderable=False)

    orgSaldoD = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='orgSaldoD',
        verbose_name=_(u'Saldo D'),
        orderable=False)

    orgModificaciones = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='orgModificaciones',
        verbose_name=_(u'Modificaciones'),
        orderable=False)

    orgTotalObligaciones = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='orgTotalObligaciones',
        verbose_name=_(u'Total Obligaciones'),
        orderable=False)

    orgSaldoDisponible = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='orgSaldoDisponible',
        verbose_name=_(u'Saldo disponible'),
        orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}


class TotalSummaryYearTable(Table):

    orgTotalObligaciones = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='orgTotalObligaciones',
        verbose_name=_(u'Total Obligaciones'))

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}
        orderable = False


class SummaryConceptTable(Table):

    concepto = tables.Column(
        accessor='concepto',
        verbose_name=_(u'Concepto'))

    funSaldoEXP = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='funSaldoEXP',
        verbose_name=_(u'Saldo EXP'),
        orderable=False)

    funSaldoFAC = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='funSaldoFAC',
        verbose_name=_(u'Saldo Facturas'),
        orderable=False)

    funSaldoA = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='funSaldoA',
        verbose_name=_(u'Saldo A'),
        orderable=False)

    funSaldoD = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='funSaldoD',
        verbose_name=_(u'Saldo D'),
        orderable=False)

    funTotalObligaciones = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='funTotalObligaciones',
        verbose_name=_(u'Total Obligaciones'),
        orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}


class BreakdownYearTable(SummaryConceptTable):

    ejercicio = tables.Column(
        accessor='ejercicio',
        verbose_name=_(u'Ejercicio'))

    concepto = tables.Column(
        accessor='concepto',
        verbose_name=_(u'Concepto'),
        orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}
        fields = ('ejercicio', )


class TotalConceptAndBreakdownTable(Table):

    funSaldoEXP = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='funSaldoEXP',
        verbose_name=_(u'Saldo total EXP'),
        orderable=False)

    funSaldoFAC = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='funSaldoFAC',
        verbose_name=_(u'Saldo total Facturas'),
        orderable=False)

    funSaldoA = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='funSaldoA',
        verbose_name=_(u'Saldo total A'),
        orderable=False)

    funSaldoD = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='funSaldoD',
        verbose_name=_(u'Saldo total D'),
        orderable=False)

    funTotalObligaciones = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='funTotalObligaciones',
        verbose_name=_(u'Total Obligaciones'),
        orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}


class DetailTable(Table):

    ejercicio = tables.Column(
        accessor='ejercicio',
        verbose_name=_(u'Ejercicio'),
        attrs={'th': {'width': '10%'}})

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
        MONEY_TEMPLATE,
        accessor='variaciones',
        verbose_name=_(u'Variaciones'),
        orderable=False)

    gastos = tables.TemplateColumn(
        MONEY_TEMPLATE,
        accessor='gastos',
        verbose_name=_(u'Gastos'),
        orderable=False)

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
        attrs = {'class': 'table table-striped table-condensed'}


class AccountingTable(Table):
    URL_TEMPLATE = '''
    <a href='{% url 'accounting_detail' record.CODIGO %}'>{{ record.NAME }}</a>
    '''

    codigo = tables.Column(
        accessor='CODIGO',
        verbose_name=_(u'Código'))

    nombre = tables.TemplateColumn(
        URL_TEMPLATE,
        accessor='NAME',
        verbose_name=_(u'Nombre'))

    claveContable = tables.Column(
        accessor='CONT_KEY',
        verbose_name=_(u'Clave contable'))

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}
        orderable = False
