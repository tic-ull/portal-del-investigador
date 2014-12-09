# -*- encoding: UTF-8 -*-

from cvn.parsers.read import (parse_cvnitem_scientificexp_property,
                              parse_cvnitem_scientificexp_agreement,
                              parse_cvnitem_scientificexp_project,
                              parse_cvnitem_teaching_phd,
                              parse_cvnitem_scientificact_congress,
                              parse_cvnitem_scientificact_production)
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

import datetime


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
        data_cvn = parse_cvnitem_scientificact_production(item)
        return super(PublicacionManager, self)._create(data_cvn, user_profile)


class CongresoManager(ProduccionManager):

    def create(self, item, user_profile):
        data_cvn = parse_cvnitem_scientificact_congress(item)
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
        data_cvn = parse_cvnitem_teaching_phd(item)
        return super(TesisDoctoralManager, self)._create(
            data_cvn, user_profile)

    def removeByUserProfile(self, user_profile):
        user_profile.tesisdoctoral_set.remove(
            *user_profile.tesisdoctoral_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()


class ProyectoManager(ProduccionManager):

    def create(self, item, user_profile):
        data_cvn = parse_cvnitem_scientificexp_project(item)
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
        data_cvn = parse_cvnitem_scientificexp_agreement(item)
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
        data_cvn = parse_cvnitem_scientificexp_property(item)
        return super(PatenteManager, self)._create(data_cvn, user_profile)

    def removeByUserProfile(self, user_profile):
        user_profile.patente_set.remove(
            *user_profile.patente_set.all())
        self.model.objects.filter(user_profile__isnull=True).delete()
