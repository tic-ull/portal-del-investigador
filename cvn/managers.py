# -*- encoding: UTF-8 -*-

from cvn.parsers.read import parse_cvnitem
from django.db import models

import datetime


class CvnItemManager(models.Manager):

    def create(self, item, user_profile):
        item = parse_cvnitem(item)
        reg = self.model(**item)
        reg.save()
        reg.user_profile.add(user_profile)
        return reg

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
