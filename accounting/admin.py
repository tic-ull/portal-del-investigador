# -*- encoding: UTF-8 -*-

from django.contrib import admin
from .models import Project, Agreement
from django.utils.translation import ugettext_lazy as _
from .sigidi import SigidiConnection


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

    def reload(self, request, queryset):
        try:
            sigidi = SigidiConnection()
            sigidi.update_projects()
            sigidi.update_agreements()
            self.message_user(
                request, _(u'Se ha actualizado el listado con éxito'))
        except:
            self.message_user(
                request, _(u'SIGIDI - Servicio no disponible'), 'error')
    reload.short_description = 'Actualizar listado desde SIGIDI'

    actions = ('reload', )
