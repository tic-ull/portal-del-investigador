# -*- encoding: UTF-8 -*-

from core.forms import PageForm
from core.models import UserProfile, Log
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from flatpages_i18n.admin import FlatPageAdmin
from flatpages_i18n.models import FlatPage_i18n, MenuItem


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0


UserAdmin.list_display = (
    'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff'
)

UserAdmin.search_fields += ('profile__documento', 'profile__rrhh_code', )

UserAdmin.inlines = [
    UserProfileInline,
]


class LogAdmin(admin.ModelAdmin):
    list_display = ('application', 'entry_type', 'user_profile', 'date')
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


FlatPage_i18n._meta.verbose_name = _("Preguntas Frecuentes")
FlatPage_i18n._meta.verbose_name_plural = _("Preguntas Frecuentes")


class PageAdmin(FlatPageAdmin):
    form = PageForm
    list_editable = []
    list_display = ('url', 'title', )
    fieldsets = (
        (None, {'fields': ('title', 'content')}),
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Log, LogAdmin)
admin.site.unregister(FlatPage_i18n)
admin.site.register(FlatPage_i18n, PageAdmin)
admin.site.unregister(MenuItem)
admin.site.unregister(Site)
