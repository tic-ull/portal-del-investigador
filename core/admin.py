# -*- encoding: UTF-8 -*-

from core.forms import PageForm
from core.models import UserProfile, Log
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0


UserAdmin.list_display = (
    'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff'
)

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


class PageAdmin(FlatPageAdmin):
    form = PageForm
    fieldsets = (
        (None, {'fields': ('title', 'content')}),
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Log, LogAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)
