# -*- encoding: UTF-8 -*-
import datetime
from django.db import models
from django.db.models import Q
from cvn import settings as stCVN
from parser_helpers import parse_scope, parse_duration, parse_authors


class ProduccionManager(models.Manager):

    search_items = ['titulo']

    # Creates a produccion with the information from insertion_dict
    # produccion: Convenio, Proyecto, Capitulo, etc.
    def _create(self, insertion_dict, user_profile):
        search_dict = self._get_search_dict(insertion_dict)
        #if not search_dict:
        #    dataSearch = {'pk': stCVN.INVALID_SEARCH}
        #table = get_model('cvn', tableName)
        objects = super(ProduccionManager, self).get_query_set()
        #TODO: Django 1.7 uncomment and comment next 2 lines
        #reg = objects.update_or_create(defaults=insertion_dict, **search_dict)[0]
        reg = objects.get_or_create(**search_dict)[0]
        objects.filter(pk=reg.id).update(**insertion_dict)
        reg.user_profile.add(user_profile)
        reg.save()

    # Creates a slice of dictionary with keys used to search
    def _get_search_dict(self, dictionary):
        out_dict = {}
        for item in self.search_items:
            if item in dictionary:
                out_dict[item] = dictionary[item]
        return out_dict

    def newInstance(self):
        pass

    def removeByUserProfile(self, user_profile):
        produccion_list = super(ProduccionManager, self).get_query_set()\
            .filter(user_profile=user_profile)
        for prod in produccion_list:
            if prod.user_profile.count() > 1:
                prod.user_profile.remove(user_profile)
            else:
                prod.delete()


class PublicacionManager(ProduccionManager):

    def byUsuariosYearTipo(self, usuarios, year, tipo):
        return super(PublicacionManager, self).get_query_set().filter(
            Q(user_profile__in=usuarios) &
            Q(fecha__year=year) &
            Q(tipo_de_produccion=tipo)
        ).distinct().order_by('fecha')


class CongresoManager(ProduccionManager):

    def byUsuariosYear(self, usuarios, year):
        return super(CongresoManager, self).get_query_set().filter(
            Q(user_profile__in=usuarios) &
            Q(fecha_realizacion__year=year)
        ).distinct().order_by('fecha_realizacion')


class TesisDoctoralManager(ProduccionManager):

    def byUsuariosYear(self, usuarios, year):
        return super(TesisDoctoralManager, self).get_query_set().filter(
            Q(user_profile__in=usuarios) &
            Q(fecha_de_lectura__year=year)
        ).distinct().order_by('fecha_de_lectura')


class ProyectoManager(ProduccionManager):

    search_items = ['denominacion_del_proyecto']

    def newInstance(self, item, user_profile):
        dataCVN = {}
        # Demonicación del Proyecto
        if item.find('Title/Name'):
            dataCVN[u'denominacion_del_proyecto'] = unicode(item.find(
                'Title/Name/Item').text.strip())
        # Posibles nodos Fecha
        if item.find('Date/StartDate'):
            node = 'StartDate'
        else:
            node = 'OnlyDate'
        # Fecha de Inicio: Día/Mes/Año
        if item.find('Date/' + node + '/DayMonthYear'):
            dataCVN[u'fecha_de_inicio'] = unicode(item.find(
                'Date/' + node + '/DayMonthYear/Item').text.strip())
        # Fecha de Inicio: Año
        elif item.find('Date/' + node + '/Year'):
            dataCVN[u'fecha_de_inicio'] = unicode(item.find(
                'Date/' + node + '/Year/Item').text.strip() + '-1-1')
        # Fecha de Finalización
        if (item.find('Date/EndDate/DayMonthYear') and
           item.find('Date/EndDate/DayMonthYear/Item').text):
            dataCVN[u'fecha_de_fin'] = unicode(item.find(
                'Date/EndDate/DayMonthYear/Item').text.strip())
        elif (item.find('Date/EndDate/Year') and
              item.find('Date/EndDate/Year/Item').text):
            dataCVN[u'fecha_de_fin'] = unicode(item.find(
                'Date/EndDate/Year/Item').text.strip() + '-1-1')
        # Duración: P <num_years> Y <num_months> M <num_days> D
        if (item.find('Date/Duration') and
           item.find('Date/Duration/Item').text):
            duration = unicode(item.find('Date/Duration/Item').text.strip())
            dataCVN.update(parse_duration(duration))
        # Autores
        dataCVN[u'autores'] = parse_authors(item.findall('Author'))
        # Dimensión Económica
        for itemXML in item.findall('EconomicDimension'):
            economic = itemXML.find('Value').attrib['code']
            dataCVN[stCVN.ECONOMIC_DIMENSION[economic]] = unicode(itemXML.find(
                'Value/Item').text.strip())
        if item.find('ExternalPK/Code'):
            dataCVN[u'cod_segun_financiadora'] = unicode(item.find(
                'ExternalPK/Code/Item').text.strip())
        # Ámbito
        dataCVN.update(parse_scope(item.find('Scope')))
        super(ProyectoManager, self)._create(dataCVN, user_profile)

    def byUsuariosYear(self, usuarios, year):
        fechaInicioMax = datetime.date(year, 12, 31)
        fechaFinMin = datetime.date(year, 1, 1)
        elements = super(ProyectoManager, self).get_query_set().filter(
            Q(user_profile__in=usuarios) &
            Q(fecha_de_inicio__isnull=False) &
            Q(fecha_de_inicio__lte=fechaInicioMax)
        ).distinct().order_by('fecha_de_inicio')
        elements_list = []
        for element in elements:
            fechaFin = element.getFechaFin()
            if fechaFin is None:
                fechaFin = element.fecha_de_inicio
            if fechaFin >= fechaFinMin:
                elements_list.append(element)
        return elements_list


class ConvenioManager(ProduccionManager):

    def byUsuariosYear(self, usuarios, year):
        fechaInicioMax = datetime.date(year, 12, 31)
        fechaFinMin = datetime.date(year, 1, 1)
        elements = super(ConvenioManager, self).get_query_set().filter(
            Q(user_profile__in=usuarios) &
            Q(fecha_de_inicio__isnull=False) &
            Q(fecha_de_inicio__lte=fechaInicioMax)
        ).distinct().order_by('fecha_de_inicio')
        elements_list = []
        for element in elements:
            fechaFin = element.getFechaFin()
            if fechaFin is None:
                fechaFin = element.fecha_de_inicio
            if fechaFin >= fechaFinMin:
                elements_list.append(element)
        return elements_list
