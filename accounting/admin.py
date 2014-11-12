# -*- encoding: UTF-8 -*-

from django.contrib import admin
from .models import Project, Agreement


@admin.register(Project, Agreement)
class AccountingAdmin(admin.ModelAdmin):

    list_display = ('code', 'gender_equality', 'free_software',)

    list_filter = ('gender_equality', 'free_software',)

    search_fields = ('code', )

    readonly_fields = ('code',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        """ Remove action delete object from list of actions """
        actions = super(AccountingAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
