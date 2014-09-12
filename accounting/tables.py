# -*- encoding: UTF-8 -*-

from core.tables import Table
from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables


class SummaryYearTable(Table):

    ejercicio = tables.Column(accessor='ejercicio',
                              verbose_name=_(u'Ejercicio'),
                              attrs={'th': {'width': '12%'}})

    inicial = tables.Column(accessor='inicial', verbose_name=_(u'Inicial'),
                            orderable=False,
                            attrs={'th': {'width': '8%'}})

    reserva = tables.Column(accessor='reserva',
                            verbose_name=_(u'Reserva de Crédito'),
                            orderable=False)

    orgSaldoRC = tables.Column(accessor='orgSaldoRC',
                               verbose_name=_(u'Saldo RC'),
                               orderable=False,
                               attrs={'th': {'width': '10%'}})

    orgSaldoA = tables.Column(accessor='orgSaldoA', verbose_name=_(u'Saldo A'),
                              orderable=False,
                              attrs={'th': {'width': '10%'}})

    orgSaldoD = tables.Column(accessor='orgSaldoD', verbose_name=_(u'Saldo D'),
                              orderable=False,
                              attrs={'th': {'width': '10%'}})

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
