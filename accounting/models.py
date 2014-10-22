# -*- encoding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Entity(models.Model):

    codigo = models.CharField(_(u'Código'), max_length=50)

    igualdad_genero = models.NullBooleanField(_(u'Igualdad de género'),
                                                 default=None)

    software_libre = models.NullBooleanField(_(u'Software libre'),
                                             default=None)

    created_at = models.DateTimeField(_(u'Creado'), auto_now_add=True)

    updated_at = models.DateTimeField(_(u'Actualizado'), auto_now=True)

    def __unicode__(self):
        return "%s" % self.codigo

    class Meta:
        abstract = True
        ordering = ["created_at"]


class Proyecto(Entity):

    class Meta:
        verbose_name_plural = _(u'Proyectos')


class Convenio(Entity):

    class Meta:
        verbose_name_plural = _(u'Convenios')
