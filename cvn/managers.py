# -*- encoding: UTF-8 -*-

from cvn.parsers.read import parse_cvnitem
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

import datetime


class CvnItemManager(models.Manager):

    search_items = ['titulo']

    def create(self, item, user_profile):
        insertion_dict = parse_cvnitem(item)
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

    def byUsuariosYear(self, usuarios, year):
        return self.model.objects.filter(
            user_profile__in=usuarios,
            fecha__year=year
        ).distinct().order_by('fecha').order_by('titulo')


class CongresoManager(CvnItemManager):

    def byUsuariosYear(self, usuarios, year):
        return super(CongresoManager, self).get_query_set().filter(
            user_profile__in=usuarios,
            fecha_de_inicio__year=year
        ).distinct().order_by('fecha_de_inicio').order_by('titulo')


class ScientificExpManager(CvnItemManager):

    def byUsuariosYear(self, usuarios, year):
        fecha_inicio_max = datetime.date(year, 12, 31)
        fecha_fin_min = datetime.date(year, 1, 1)
        elements = super(ScientificExpManager, self).get_query_set().filter(
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
