# -*- encoding: UTF-8 -*-

#
#    Copyright 2014-2015
#
#      STIC-Investigación - Universidad de La Laguna (ULL) <gesinv@ull.edu.es>
#
#    This file is part of Portal del Investigador.
#
#    Portal del Investigador is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    Portal del Investigador is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Portal del Investigador.  If not, see
#    <http://www.gnu.org/licenses/>.
#

from .forms import PageForm
from .models import UserProfile, Log
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.flatpages.admin import FlatPageAdmin  # Don't delete
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from modeltranslation.translator import translator, TranslationOptions


# Options for the flatpages (faq)
class FlatPageTranslationOptions(TranslationOptions):
        fields = ('title', 'content',)

translator.register(FlatPage, FlatPageTranslationOptions)


class CustomFlatPageAdmin(TranslationAdmin):
    form = PageForm
    list_editable = []
    list_display = ('url', 'title', )
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('title', 'content')}),
    )

FlatPage._meta.verbose_name = _("Preguntas Frecuentes")
FlatPage._meta.verbose_name_plural = _("Preguntas Frecuentes")


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0
    readonly_fields = ('rrhh_code', )


def remove_fieldsets(cls, field_name):
    """Remove a field from the fieldset of an Admin class"""
    lst = list(cls.fieldsets)
    for sets in lst:
        if field_name in sets[1]['fields']:
            field = list(sets[1]['fields'])
            field.remove(field_name)
            sets[1]['fields'] = tuple(field)
    return tuple(lst)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email',
                    'is_active', 'is_staff')

    readonly_fields = ('first_name', 'last_name', 'email')

    search_fields = UserAdmin.search_fields + (
        'profile__documento', 'profile__rrhh_code', )

    inlines = [
        UserProfileInline,
    ]

    fieldsets = remove_fieldsets(UserAdmin, 'user_permissions')

    list_filter = UserAdmin.list_filter + ('groups__name', )


class LogAdmin(admin.ModelAdmin):

    list_display = ('application', 'entry_type', 'user_profile', 'date')

    list_filter = ('entry_type', 'application')

    search_fields = (
        'user_profile__user__username', 'user_profile__documento',
    )

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

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Log, LogAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)
admin.site.unregister(Site)
