# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.models import (Congreso, Proyecto, Convenio, TesisDoctoral, Articulo,
                        Libro, CVN, Capitulo)
from core.models import UserProfile
from django.contrib import admin
import logging

logger = logging.getLogger(__name__)


class CVNAdmin(admin.ModelAdmin):
    model = CVN
    form = UploadCVNForm
    list_display = (
        'cvn_file', 'user_profile', 'fecha', 'status', 'xml_file',
        'is_inserted', )
    list_filter = ('status', 'is_inserted', )
    search_fields = (
        'user_profile__user__username',
        'user_profile__documento',
        'user_profile__rrhh_code',
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
    list_display = ('user', 'documento', 'rrhh_code', )
    search_fields = ['user__username', 'documento', 'rrhh_code', ]
    inlines = [
        CVNInline,
    ]

    def has_add_permission(self, request):
        return False


class ProductionAdmin(admin.ModelAdmin):
    search_fields = (
        'titulo',
        'user_profile__user__username',
        'user_profile__documento',
        'user_profile__user__first_name',
        'user_profile__user__last_name',
        'user_profile__rrhh_code',
    )
    ordering = ('created_at',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CVN, CVNAdmin)
admin.site.register(Articulo, ProductionAdmin)
admin.site.register(Libro, ProductionAdmin)
admin.site.register(Capitulo, ProductionAdmin)
admin.site.register(TesisDoctoral, ProductionAdmin)
admin.site.register(Congreso, ProductionAdmin)
admin.site.register(Proyecto, ProductionAdmin)
admin.site.register(Convenio, ProductionAdmin)
