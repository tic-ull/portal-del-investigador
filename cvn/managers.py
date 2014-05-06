# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from django.db import models
from django.db.models import Q
from parser_helpers import (parse_scope, parse_authors,
                            parse_publicacion_location, parse_date,
                            parse_produccion_subtype, parse_date_interval,
                            parse_produccion_id)
import datetime


class ProduccionManager(models.Manager):

    search_items = ['titulo']

    # Creates a produccion with the information from insertion_dict
    # produccion: Convenio, Proyecto, Capitulo, etc.
    def _create(self, insertion_dict, user_profile):
        search_dict = self._get_search_dict(insertion_dict)
        if not len(search_dict):
            return
        objects = super(ProduccionManager, self).get_query_set()
        # TODO: Django 1.7 uncomment and delete next 3 lines
        # reg = objects.update_or_create(defaults=insertion_dict,
        #                               **search_dict)[0]
        reg = objects.get_or_create(**search_dict)[0]
        objects.filter(pk=reg.id).update(**insertion_dict)
        reg = objects.get(pk=reg.id)
        reg.user_profile.add(user_profile)
        reg.save()
        return reg

    # Creates a slice of dictionary with keys used to search
    def _get_search_dict(self, dictionary):
        out_dict = {}
        for item in self.search_items:
            if item in dictionary:
                out_dict[item + '__iexact'] = dictionary[item]
        return out_dict

    def create(self, item, user_profile):
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

    def create(self, item, user_profile):
        dataCVN = {}
        dataCVN[u'tipo_de_produccion'] = parse_produccion_subtype(item)
        if item.find('Title/Name'):
            dataCVN[u'titulo'] = unicode(item.find(
                'Title/Name/Item').text.strip())
        if (item.find('Link/Title/Name') and
           item.find('Link/Title/Name/Item').text):
            dataCVN[u'nombre_publicacion'] = unicode(item.find(
                'Link/Title/Name/Item').text.strip())
        dataCVN[u'autores'] = parse_authors(item.findall(
            'Author'))
        dataCVN.update(parse_publicacion_location(item.find('Location')))
        dataCVN[u'fecha'] = parse_date(item.find('Date'))
        dataCVN['issn'] = parse_produccion_id(item.findall('ExternalPK'),
                                              stCVN.PRODUCCION_ID_CODE['ISSN'])
        dataCVN['isbn'] = parse_produccion_id(item.findall('ExternalPK'),
                                              stCVN.PRODUCCION_ID_CODE['ISBN'])
        return super(PublicacionManager, self)._create(dataCVN, user_profile)

    def byUsuariosYearTipo(self, usuarios, year, tipo):
        return super(PublicacionManager, self).get_query_set().filter(
            Q(user_profile__in=usuarios) &
            Q(fecha__year=year) &
            Q(tipo_de_produccion=tipo)
        ).distinct().order_by('fecha')


class CongresoManager(ProduccionManager):

    def create(self, item, user_profile):
        dataCVN = {}
        if item.find('Title/Name'):
            dataCVN[u'titulo'] = unicode(item.find(
                'Title/Name/Item').text.strip())
        for itemXML in item.findall('Link'):
            if itemXML.find(
                'CvnItemID/CodeCVNItem/Item'
            ).text.strip() == stCVN.DATA_CONGRESO:
                if (itemXML.find('Title/Name') and
                   itemXML.find('Title/Name/Item').text):
                    dataCVN[u'nombre_del_congreso'] = unicode(itemXML.find(
                        'Title/Name/Item').text.strip())

                date_node = itemXML.find('Date')
                (dataCVN['fecha_de_inicio'], dataCVN['fecha_de_fin'],
                    duracion) = parse_date_interval(date_node)

                if itemXML.find('Place/City'):
                    dataCVN[u'ciudad_de_realizacion'] = unicode(itemXML.find(
                        'Place/City/Item').text.strip())
                # Ámbito
                dataCVN.update(parse_scope(itemXML.find('Scope')))
        dataCVN[u'autores'] = parse_authors(item.findall('Author'))
        return super(CongresoManager, self)._create(dataCVN, user_profile)

    def byUsuariosYear(self, usuarios, year):
        return super(CongresoManager, self).get_query_set().filter(
            Q(user_profile__in=usuarios) &
            Q(fecha_de_inicio__year=year)
        ).distinct().order_by('fecha_de_inicio')


class TesisDoctoralManager(ProduccionManager):

    def create(self, item, user_profile):
        dataCVN = {}
        dataCVN[u'titulo'] = unicode(item.find(
            'Title/Name/Item').text.strip())
        dataCVN[u'universidad_que_titula'] = unicode(item.find(
            'Entity/EntityName/Item').text.strip())
        dataCVN[u'autor'] = parse_authors(
            item.findall('Author'))
        dataCVN[u'codirector'] = parse_authors(
            item.findall('Link/Author'))
        dataCVN['fecha_de_lectura'] = parse_date(item.find('Date'))
        return super(TesisDoctoralManager, self)._create(dataCVN, user_profile)

    def byUsuariosYear(self, usuarios, year):
        return super(TesisDoctoralManager, self).get_query_set().filter(
            Q(user_profile__in=usuarios) &
            Q(fecha_de_lectura__year=year)
        ).distinct().order_by('fecha_de_lectura')


class ProyectoManager(ProduccionManager):

    search_items = ['denominacion_del_proyecto']

    def create(self, item, user_profile):
        dataCVN = {}
        # Demonicación del Proyecto
        if item.find('Title/Name'):
            dataCVN[u'denominacion_del_proyecto'] = unicode(item.find(
                'Title/Name/Item').text.strip())

        date_node = item.find('Date')
        (dataCVN['fecha_de_inicio'], dataCVN['fecha_de_fin'],
            dataCVN['duracion']) = parse_date_interval(date_node)

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
        return super(ProyectoManager, self)._create(dataCVN, user_profile)

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

    search_items = ['denominacion_del_proyecto']

    def create(self, item, user_profile):

        dataCVN = {}
        # Demonicación del Proyecto
        if item.find('Title/Name'):
            dataCVN[u'denominacion_del_proyecto'] = unicode(item.find(
                'Title/Name/Item').text.strip())

        date_node = item.find('Date')
        (dataCVN['fecha_de_inicio'], dataCVN['fecha_de_fin'],
            dataCVN['duracion']) = parse_date_interval(date_node)

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
        return super(ConvenioManager, self)._create(dataCVN, user_profile)

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
