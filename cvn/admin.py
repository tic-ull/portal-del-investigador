# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.models import (Congreso, Proyecto, Convenio, TesisDoctoral, Articulo,
                        Libro, CVN, Capitulo)
from core.models import UserProfile
from django.contrib import admin
# Flatpages TinyMCE
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
#
import logging

logger = logging.getLogger(__name__)


class CVNAdmin(admin.ModelAdmin):
    model = CVN
    form = UploadCVNForm
    list_display = (
        'cvn_file', 'user_profile', 'fecha_cvn', 'status', 'xml_file',
    )
    list_filter = ('status',)
    search_fields = (
        'user_profile__user__username',
        'user_profile__documento',
        'user_profile__user__first_name',
        'user_profile__user__last_name'
    )
    ordering = ('-updated_at', )

    def has_add_permission(self, request):
        return False


class CVNInline(admin.StackedInline):
    model = CVN
    form = UploadCVNForm


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        CVNInline,
    ]

    def has_add_permission(self, request):
        return False


class PublicationAdmin(admin.ModelAdmin):
    search_fields = ('titulo',
                     'usuario__nombre',
                     'usuario__primer_apellido',
                     'usuario__segundo_apellido',
                     'usuario__documento',)
    ordering = ('created_at',)


class ProyectoConvenioAdmin(admin.ModelAdmin):
    search_fields = ('denominacion_del_proyecto',
                     'usuario__nombre',
                     'usuario__primer_apellido',
                     'usuario__segundo_apellido',
                     'usuario__documento',)
    ordering = ('created_at',)


class PageForm(FlatpageForm):

    class Meta:
        model = FlatPage
        widgets = {
            'content': TinyMCE(attrs={'cols': 100, 'rows': 15}),
        }


class PageAdmin(FlatPageAdmin):
    form = PageForm


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CVN, CVNAdmin)
admin.site.register(Articulo, PublicationAdmin)
admin.site.register(Libro, PublicationAdmin)
admin.site.register(Capitulo, PublicationAdmin)
admin.site.register(TesisDoctoral, PublicationAdmin)
admin.site.register(Congreso, PublicationAdmin)
admin.site.register(Proyecto, ProyectoConvenioAdmin)
admin.site.register(Convenio, ProyectoConvenioAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)
