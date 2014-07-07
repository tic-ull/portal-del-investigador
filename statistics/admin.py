# -*- encoding: UTF-8 -*-

from django.contrib import admin
from models import ProfessionalCategory


class ProfessionalCategoryAdmin(admin.ModelAdmin):
    model = ProfessionalCategory
    list_display = ('code', 'name', 'is_cvn_required', )
    list_filter = ('is_cvn_required', )
    search_fields = ('code', 'name', )
    readonly_fields = ('code', 'name', )
    ordering = ('name', )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        """ Remove action delete object from list of actions """
        actions = super(ProfessionalCategoryAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(ProfessionalCategory, ProfessionalCategoryAdmin)
