# -*- encoding: UTF-8 -*-

from django.db import models
from parser_helpers import (parse_scope, parse_authors, parse_places,
                            parse_publicacion_location, parse_date,
                            parse_date_interval, parse_economic,
                            parse_entities, parse_produccion_id, parse_title)
from django.core.exceptions import ObjectDoesNotExist
import datetime
import settings as st_cvn


class ProduccionManager(models.Manager):

    search_items = ['titulo']

    # Creates a produccion with the information from insertion_dict
    # produccion: Convenio, Proyecto, Capitulo, etc.
    def _create(self, insertion_dict, user_profile):
        search_dict = self._get_search_dict(insertion_dict)
        if not len(search_dict):
            reg = self.model(**insertion_dict)
        else:
            try:
                reg = self.model.objects.get(**search_dict)
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
            if item in dictionary and dictionary[item] is not None:
                out_dict[item + '__iexact'] = dictionary[item]
        return out_dict

    def create(self, item, user_profile):
        pass

    def removeByUserProfile(self, user_profile):
        pass

    def byUsuariosYear(self, usuarios, year):
        return self.model.objects.filter(
            user_profile__in=usuarios,
            fecha__year=year
        ).distinct().order_by('fecha').order_by('titulo')


class PublicacionManager(ProduccionManager):

    def create(self, item, user_profile):
        data_cvn = dict()
        data_cvn['titulo'] = parse_title(item)
        if (item.find('Link/Title/Name') and
           item.find('Link/Title/Name/Item').text):
            data_cvn[u'nombre_publicacion'] = unicode(item.find(
                'Link/Title/Name/Item').text.strip())
        data_cvn[u'autores'] = parse_authors(item.findall(
            'Author'))
        data_cvn.update(parse_publicacion_location(item.find('Location')))
        data_cvn['fecha'] = parse_date(item.find('Date'))
        data_cvn['issn'] = parse_produccion_id(
            item.findall('ExternalPK'),
            st_cvn.PRODUCCION_ID_CODE['ISSN'])
        data_cvn['isbn'] = parse_produccion_id(
            item.findall('ExternalPK'),
            st_cvn.PRODUCCION_ID_CODE['ISBN'])
        data_cvn['deposito_legal'] = parse_produccion_id(item.findall(
            'ExternalPK'), st_cvn.PRODUCCION_ID_CODE['DEPOSITO_LEGAL'])
        return super(PublicacionManager, self)._create(data_cvn, user_profile)


class CongresoManager(ProduccionManager):

    def create(self, item, user_profile):
        data_cvn = dict()
        data_cvn['titulo'] = parse_title(item)
        for itemXML in item.findall('Link'):
            if itemXML.find(
                'CvnItemID/CodeCVNItem/Item'
            ).text.strip() == st_cvn.DATA_CONGRESO:
                if (itemXML.find('Title/Name') and
                   itemXML.find('Title/Name/Item').text):
                    data_cvn[u'nombre_del_congreso'] = unicode(itemXML.find(
                        'Title/Name/Item').text.strip())

                date_node = itemXML.find('Date')
                (data_cvn['fecha_de_inicio'], data_cvn['fecha_de_fin'],
                    duracion) = parse_date_interval(date_node)

                if itemXML.find('Place/City'):
                    data_cvn[u'ciudad_de_realizacion'] = unicode(itemXML.find(
                        'Place/City/Item').text.strip())
                # Ámbito
                data_cvn.update(parse_scope(itemXML.find('Scope')))
        data_cvn[u'autores'] = parse_authors(item.findall('Author'))
        return super(CongresoManager, self)._create(data_cvn, user_profile)

    def byUsuariosYear(self, usuarios, year):
        return super(CongresoManager, self).get_query_set().filter(
            user_profile__in=usuarios,
            fecha_de_inicio__year=year
        ).distinct().order_by('fecha_de_inicio').order_by('titulo')

    def removeByUserProfile(self, user_profile):
        user_profile.congreso_set.remove(
            *user_profile.congreso_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()


class TesisDoctoralManager(ProduccionManager):

    def create(self, item, user_profile):
        data_cvn = dict()
        data_cvn['titulo'] = parse_title(item)
        node = item.find('Entity/EntityName/Item')
        if node is not None:
            data_cvn[u'universidad_que_titula'] = unicode(node.text.strip())
        data_cvn[u'autor'] = parse_authors(
            item.findall('Author'))
        data_cvn[u'codirector'] = parse_authors(
            item.findall('Link/Author'))
        data_cvn['fecha'] = parse_date(item.find('Date'))
        return super(TesisDoctoralManager, self)._create(
            data_cvn, user_profile)

    def removeByUserProfile(self, user_profile):
        user_profile.tesisdoctoral_set.remove(
            *user_profile.tesisdoctoral_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()


class ProyectoManager(ProduccionManager):

    def create(self, item, user_profile):
        data_cvn = dict()
        data_cvn['titulo'] = parse_title(item)
        date_node = item.find('Date')
        (data_cvn['fecha_de_inicio'], data_cvn['fecha_de_fin'],
            data_cvn['duracion']) = parse_date_interval(date_node)
        # Autores
        data_cvn[u'autores'] = parse_authors(item.findall('Author'))
        data_cvn.update(parse_economic(item.findall('EconomicDimension')))
        if item.find('ExternalPK/Code'):
            data_cvn[u'cod_segun_financiadora'] = unicode(item.find(
                'ExternalPK/Code/Item').text.strip())
        # Ámbito
        data_cvn.update(parse_scope(item.find('Scope')))
        return super(ProyectoManager, self)._create(data_cvn, user_profile)

    def byUsuariosYear(self, usuarios, year):
        fecha_inicio_max = datetime.date(year, 12, 31)
        fecha_fin_min = datetime.date(year, 1, 1)
        elements = super(ProyectoManager, self).get_query_set().filter(
            user_profile__in=usuarios,
            fecha_de_inicio__isnull=False,
            fecha_de_inicio__lte=fecha_inicio_max
        ).distinct().order_by('fecha_de_inicio').order_by('titulo')
        elements_list = []
        for element in elements:
            fecha_fin = element.fecha_de_fin
            if fecha_fin is None:
                fecha_fin = element.fecha_de_inicio
            if fecha_fin >= fecha_fin_min:
                elements_list.append(element)
        return elements_list

    def removeByUserProfile(self, user_profile):
        user_profile.proyecto_set.remove(
            *user_profile.proyecto_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()


class ConvenioManager(ProduccionManager):

    def create(self, item, user_profile):
        data_cvn = dict()
        data_cvn['titulo'] = parse_title(item)
        date_node = item.find('Date')
        (data_cvn['fecha_de_inicio'], data_cvn['fecha_de_fin'],
            data_cvn['duracion']) = parse_date_interval(date_node)
        # Autores
        data_cvn[u'autores'] = parse_authors(item.findall('Author'))
        data_cvn.update(parse_economic(item.findall('EconomicDimension')))
        if item.find('ExternalPK/Code'):
            data_cvn[u'cod_segun_financiadora'] = unicode(item.find(
                'ExternalPK/Code/Item').text.strip())
        # Ámbito
        data_cvn.update(parse_scope(item.find('Scope')))
        return super(ConvenioManager, self)._create(data_cvn, user_profile)

    def byUsuariosYear(self, usuarios, year):
        fecha_inicio_max = datetime.date(year, 12, 31)
        fecha_fin_min = datetime.date(year, 1, 1)
        elements = super(ConvenioManager, self).get_query_set().filter(
            user_profile__in=usuarios,
            fecha_de_inicio__isnull=False,
            fecha_de_inicio__lte=fecha_inicio_max
        ).distinct().order_by('fecha_de_inicio').order_by('titulo')
        elements_list = []
        for element in elements:
            fecha_fin = element.fecha_de_fin
            if fecha_fin is None:
                fecha_fin = element.fecha_de_inicio
            if fecha_fin >= fecha_fin_min:
                elements_list.append(element)
        return elements_list

    def removeByUserProfile(self, user_profile):
        user_profile.convenio_set.remove(
            *user_profile.convenio_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()


class PatenteManager(ProduccionManager):

    def create(self, item, user_profile):
        data_cvn = dict()
        data_cvn['titulo'] = parse_title(item)
        dates = item.findall('Date')
        for date in dates:                              # There can be 2 dates
            parsed_date = parse_date(date)
            date_type = date.find("Moment/Item").text
            if date_type == st_cvn.REGULAR_DATE_CODE:   # Date of request
                data_cvn['fecha'] = parsed_date
            else:                                       # And date of granting
                data_cvn['fecha_concesion'] = parsed_date
        data_cvn['num_solicitud'] = parse_produccion_id(item.findall(
            'ExternalPK'), st_cvn.PRODUCCION_ID_CODE['SOLICITUD'])
        (data_cvn['lugar_prioritario'], data_cvn['lugares']) = parse_places(
            item.findall("Place"))
        data_cvn[u'autores'] = parse_authors(item.findall('Author'))
        (data_cvn['entidad_titular'], data_cvn['empresas']) = parse_entities(
            item.findall("Entity"))
        return super(PatenteManager, self)._create(data_cvn, user_profile)

    def removeByUserProfile(self, user_profile):
        user_profile.patente_set.remove(
            *user_profile.patente_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()
