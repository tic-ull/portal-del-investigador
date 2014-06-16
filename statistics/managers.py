# -*- encoding: UTF-8 -*-

from django.db import models


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
