# -*- encoding: UTF-8 -*-

from django.conf import settings as st
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import json
import urllib


class StatsManager(models.Manager):

    def create(self, name, code, members, commit=False):
        model = self.model(code=code)
        model.update(name, members, commit)
        return model

    def create_all(self, stats):
        object_list = []
        for stat in stats:
            object_list.append(self.create(
                stat['departamento']['nombre'],
                stat['departamento']['cod_departamento'],
                stat['miembros']))
        return super(StatsManager, self).bulk_create(object_list)


class ProfessionalCategoryManager(models.Manager):

    def update(self, past_days=0):
        categories = json.loads(
            urllib.urlopen(st.WS_CATEGORY % past_days).read())
        for category in categories:
            try:
                pc = self.model.objects.get(code=category['id'])
                if pc.name != category['descripcion']:
                    pc.name = category['descripcion']
                    pc.save()
            except ObjectDoesNotExist:
                self.model.objects.create(
                    **{'name': category['descripcion'],
                       'code': category['id']})
