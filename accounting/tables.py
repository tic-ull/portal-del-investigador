# -*- encoding: UTF-8 -*-

from core.tables import Table
from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables


class SummaryYearTable(Table):

    ejercicio = tables.Column(accessor='ejercicio',
                              verbose_name=_(u'Ejercicio'))

    inicial = tables.Column(accessor='inicial', verbose_name=_(u'Inicial'),
                            orderable=False)

    reserva = tables.Column(accessor='reserva',
                            verbose_name=_(u'Reserva de Crédito'),
                            orderable=False)

    orgSaldoRC = tables.Column(accessor='orgSaldoRC',
                               verbose_name=_(u'Saldo RC'),
                               orderable=False)

    orgSaldoA = tables.Column(accessor='orgSaldoA', verbose_name=_(u'Saldo A'),
                              orderable=False)

    orgSaldoD = tables.Column(accessor='orgSaldoD', verbose_name=_(u'Saldo D'),
                              orderable=False)

    orgModificaciones = tables.Column(accessor='orgModificaciones',
                                      verbose_name=_(u'Modificaciones'),
                                      orderable=False)

    orgTotalObligaciones = tables.Column(accessor='orgTotalObligaciones',
                                         verbose_name=_(u'Total Obligaciones'),
                                         orderable=False)

    orgSaldoDisponible = tables.Column(accessor='orgSaldoDisponible',
                                       verbose_name=_(u'Saldo disponible'),
                                       orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}


class TotalSummaryYearTable(Table):

    orgTotalObligaciones = tables.Column(accessor='orgTotalObligaciones',
                                         verbose_name=_(u'Total Obligaciones'),
                                         orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}


class SummaryConceptTable(Table):

    concepto = tables.Column(accessor='concepto', verbose_name=_(u'Concepto'))

    funSaldoEXP = tables.Column(accessor='funSaldoEXP',
                                verbose_name=_(u'Saldo EXP'),
                                orderable=False)

    funSaldoFAC = tables.Column(accessor='funSaldoFAC',
                                verbose_name=_(u'Saldo Facturas'),
                                orderable=False)

    funSaldoA = tables.Column(accessor='funSaldoA',
                              verbose_name=_(u'Saldo A'),
                              orderable=False)

    funSaldoD = tables.Column(accessor='funSaldoD',
                              verbose_name=_(u'Saldo D'),
                              orderable=False)

    funTotalObligaciones = tables.Column(accessor='funTotalObligaciones',
                                         verbose_name=_(u'Total Obligaciones'),
                                         orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}


class BreakdownYearTable(SummaryConceptTable):

    ejercicio = tables.Column(accessor='ejercicio',
                              verbose_name=_(u'Ejercicio'))

    concepto = tables.Column(accessor='concepto',
                             verbose_name=_(u'Concepto'),
                             orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}
        fields = ('ejercicio', )


class TotalConceptAndBreakdownTable(Table):

    funSaldoEXP = tables.Column(accessor='funSaldoEXP',
                                verbose_name=_(u'Saldo total EXP'),
                                orderable=False)

    funSaldoFAC = tables.Column(accessor='funSaldoFAC',
                                verbose_name=_(u'Saldo total Facturas'),
                                orderable=False)

    funSaldoA = tables.Column(accessor='funSaldoA',
                              verbose_name=_(u'Saldo total A'),
                              orderable=False)

    funSaldoD = tables.Column(accessor='funSaldoD',
                              verbose_name=_(u'Saldo total D'),
                              orderable=False)

    funTotalObligaciones = tables.Column(accessor='funTotalObligaciones',
                                         verbose_name=_(u'Total Obligaciones'),
                                         orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}


class DetailTable(Table):

    ejercicio = tables.Column(accessor='ejercicio',
                              verbose_name=_(u'Ejercicio'),
                              attrs={'th': {'width': '10%'}})

    numero = tables.Column(accessor='numero',
                           verbose_name=_(u'Número'))

    tipo = tables.Column(accessor='tipo', verbose_name=_(u'Tipo'),
                         orderable=False)

    proveedor = tables.Column(accessor='proveedor',
                              verbose_name=_(u'Proveedor'),
                              orderable=False)

    descripcion = tables.Column(accessor='descripcion',
                                verbose_name=_(u'Descripción'),
                                orderable=False)

    concepto = tables.Column(accessor='concepto',
                             verbose_name=_(u'Concepto'),
                             orderable=False)

    variaciones = tables.Column(accessor='variaciones',
                                verbose_name=_(u'Variaciones'),
                                orderable=False)

    gastos = tables.Column(accessor='gastos', verbose_name=_(u'Gastos'),
                           orderable=False)

    asiento = tables.Column(accessor='asiento', verbose_name=_(u'Asiento'),
                            orderable=False)

    validacion = tables.Column(accessor='validacion',
                               verbose_name=_(u'Validación'),
                               orderable=False)

    pago = tables.Column(accessor='pago', verbose_name=_(u'Pago'),
                         orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-condensed'}
