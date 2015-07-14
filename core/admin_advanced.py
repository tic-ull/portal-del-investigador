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

from .forms import GroupAdminForm, CustomUserForm
from .forms import PageForm
from .models import UserProfile, Log
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.flatpages.admin import FlatPageAdmin  # Don't delete
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django_cas.views import logout
from modeltranslation.admin import TranslationAdmin
from modeltranslation.translator import translator, TranslationOptions
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)



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


removal_text = _(u'Se ha deshabilitado la configuración de permisos por'
                 u' usuario, ya que deben configurarse por grupos.')

removal_message = loader.get_template('core/partials/message_box.html').render(
    Context({'message_content': removal_text}))


def remove_fieldsets(cls, field_name, message=None, new_field=None):
    """Remove a field from the fieldset of an Admin class"""
    lst = list(cls.fieldsets)
    for sets in lst:
        if field_name in sets[1]['fields']:
            field = list(sets[1]['fields'])
            field.remove(field_name)
            if new_field is not None:
                field.append(new_field)
            sets[1]['fields'] = tuple(field)
            if message is not None:
                sets[1]['description'] = message
    return tuple(lst)


class CustomUserAdmin(UserAdmin):

    form = CustomUserForm

    list_display = ('username', 'first_name', 'last_name', 'email',
                    'is_active', 'is_staff')

    readonly_fields = ('first_name', 'last_name', 'email')

    search_fields = UserAdmin.search_fields + (
        'profile__documento', 'profile__rrhh_code', )

    inlines = [
        UserProfileInline,
    ]

    fieldsets = remove_fieldsets(
        UserAdmin, 'user_permissions', removal_message, 'permissions')

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


class CustomGroupAdmin(GroupAdmin):
    form = GroupAdminForm

    def membership(self):
        return self.user_set.count()
    membership.short_description = _(u"Número de miembros")
    membership.allow_tags = True

    list_display = ('name', membership, )


def change_dni(user_profile, new_dni):
    user_profile.documento = new_dni
    user_profile.save()
    try:
        #Latest CVNs
        cvn = user_profile.cvn
        f_pdf = File(open(cvn.cvn_file.path))
        cvn.cvn_file.save(u'fake.pdf',f_pdf)
        f_xml = File(open(cvn.xml_file.path))
        cvn.xml_file.save(u'fake.xml',f_xml)
        cvn.save()
    except ObjectDoesNotExist:
        pass
    try:
        #Old CVNs
        for oldcvn in user_profile.oldcvnpdf_set.all():
            f_pdf = File(open(oldcvn.cvn_file.path))

            filename = 'CVN-%s-%s.pdf'%(user_profile.documento, oldcvn.uploaded_at.strftime('%Y-%m-%d-%Hh%Mm%Ss'))
            oldcvn.cvn_file.save(filename, f_pdf)
    except ObjectDoesNotExist:
        pass

admin.site.login = login_required(admin.site.login)
admin.site.logout = logout
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(Log, LogAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)
admin.site.unregister(Site)
