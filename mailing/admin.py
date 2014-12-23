# -*- encoding: UTF-8 -*-

from .forms import EmailForm
from .models import Email
from django.contrib import admin


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):

    readonly_fields = ('entry_type', )

    form = EmailForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        """ Remove action delete object from list of actions """
        actions = super(EmailAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
