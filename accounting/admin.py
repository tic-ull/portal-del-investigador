# -*- encoding: UTF-8 -*-

from accounting.sigidi import SigidiConnection
from django.conf.urls import patterns #  , url
from django.contrib import admin
# from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from models import (Proyecto, Convenio,)


class DataSigidiAdmin(admin.ModelAdmin):

    list_display = ('codigo', 'igualdad_genero', 'software_libre',)

    list_filter = ('igualdad_genero', 'software_libre',)

    search_fields = ['codigo']

    readonly_fields = ('codigo',)

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

    # def get_urls(self):
    #     urls = super(DataSigidiAdmin, self).get_urls()
    #     my_urls = patterns('',
    #                        (r'^update/$',
    #                         self.admin_site.admin_view(self.update_view)))
    #     return my_urls + urls


class ProjectAdmin(DataSigidiAdmin):
    # change_form_template = 'change_form_local.html'
    def get_urls(self):
        urls = super(ProjectAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^update/$',
                            self.admin_site.admin_view(self.update_view)))
        return my_urls + urls

    def update_view(self, request):
        print request.path
        sigidi = SigidiConnection()
        sigidi.update_get_all_projects()
        return redirect(request.path)


class ConvenioAdmin(DataSigidiAdmin):
    def update_view(self):
        sigidi = SigidiConnection()
        sigidi.update_get_all_convenios()
        return redirect('admin/accounting/convenio/')

admin.site.register(Proyecto, ProjectAdmin)
#admin.site.register(Convenio, ConvenioAdmin)

