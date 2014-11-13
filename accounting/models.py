# -*- encoding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Entity(models.Model):

    code = models.CharField(_(u'Código'), max_length=100, unique=True)

    gender_equality = models.NullBooleanField(
        _(u'Igualdad de género'), default=None)

    free_software = models.NullBooleanField(
        _(u'Software Libre'), default=None)

    created_at = models.DateTimeField(_(u'Creado'), auto_now_add=True)

    updated_at = models.DateTimeField(_(u'Actualizado'), auto_now=True)

    def __unicode__(self):
        return u'%s' % self.code

    def __eq__(self, other):
        return self.code == other.code

    class Meta:
        abstract = True


class Project(Entity):

    class Meta:
        verbose_name_plural = _(u'Proyectos')
        ordering = ['-code']


class Agreement(Entity):

    class Meta:
        verbose_name_plural = _(u'Convenios')
        ordering = ['-code']
