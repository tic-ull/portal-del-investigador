# -*- encoding: UTF-8 -*-

from core.models import Log
from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets


class LogAdmin(admin.ModelAdmin):
    list_filter = ('entry_type', 'application')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        """ Remove action delete object from list of actions """
        actions = super(LogAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        return tuple(Log._meta.get_all_field_names())


admin.site.register(Log, LogAdmin)
