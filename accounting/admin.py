# -*- encoding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from models import (Proyecto, Convenio,)


def update_data(modeladmin, request, queryset):
    print "Actualizando desde SIGIDI"
update_data.short_description = _(u'Actualizar producción')


class DataSigidiAdmin(admin.ModelAdmin):

    list_display = ('codigo', 'igualdad_genero', 'software_libre',)

    list_filter = ('igualdad_genero', 'software_libre',)

    search_fields = ['codigo']

    readonly_fields = ('codigo',)

    actions = [update_data]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        """ Remove action delete object from list of actions """
        actions = super(DataSigidiAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Proyecto, DataSigidiAdmin)
admin.site.register(Convenio, DataSigidiAdmin)
