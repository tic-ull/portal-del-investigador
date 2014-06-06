# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from django.db import models
from django.db.models import Q
from parser_helpers import (parse_scope, parse_authors,
                            parse_publicacion_location, parse_date,
                            parse_produccion_subtype, parse_date_interval,
                            parse_produccion_id)
import datetime
from django.core.exceptions import ObjectDoesNotExist


class ProduccionManager(models.Manager):

    search_items = ['titulo']

    # Creates a produccion with the information from insertion_dict
    # produccion: Convenio, Proyecto, Capitulo, etc.
    def _create(self, insertion_dict, user_profile):
        search_dict = self._get_search_dict(insertion_dict)
        if not len(search_dict):
            return
        objects = super(ProduccionManager, self).get_query_set()
        # Django 1.7 could use bellow code, if user_profile.add
        # can be added to the query it is a possibility:
        # reg = objects.update_or_create(defaults=insertion_dict,
        #                               **search_dict)[0]
        try:
            reg = objects.get(**search_dict)
        except ObjectDoesNotExist:
            reg = self.model(**insertion_dict)
        else:
            for key, value in insertion_dict.items():
                setattr(reg, key, value)
        reg.save()
        reg.user_profile.add(user_profile)
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
        pass


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


class ArticuloManager(PublicacionManager):

    def removeByUserProfile(self, user_profile):
        user_profile.articulo_set.remove(
            *user_profile.articulo_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()


class LibroManager(PublicacionManager):

    def removeByUserProfile(self, user_profile):
        user_profile.libro_set.remove(
            *user_profile.libro_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()


class CapituloManager(PublicacionManager):

    def removeByUserProfile(self, user_profile):
        user_profile.capitulo_set.remove(
            *user_profile.capitulo_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()


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

    def removeByUserProfile(self, user_profile):
        user_profile.congreso_set.remove(
            *user_profile.congreso_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()


class TesisDoctoralManager(ProduccionManager):

    def create(self, item, user_profile):
        dataCVN = {}
        node = item.find('Title/Name/Item')
        if node is not None:
            dataCVN[u'titulo'] = unicode(node.text.strip())
        node = item.find('Entity/EntityName/Item')
        if node is not None:
            dataCVN[u'universidad_que_titula'] = unicode(node.text.strip())
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

    def removeByUserProfile(self, user_profile):
        user_profile.tesisdoctoral_set.remove(
            *user_profile.tesisdoctoral_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()


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

    def removeByUserProfile(self, user_profile):
        user_profile.proyecto_set.remove(
            *user_profile.proyecto_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()


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

    def removeByUserProfile(self, user_profile):
        user_profile.convenio_set.remove(
            *user_profile.convenio_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()
