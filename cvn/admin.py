# -*- encoding: UTF-8 -*-

from cvn.forms import UploadCVNForm
from cvn.models import (Congreso, Proyecto, Convenio, TesisDoctoral, Articulo,
                        Libro, CVN, Capitulo)
from core.models import UserProfile
from django.contrib import admin
# Flatpages TinyMCE
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage, Site
from django.forms.widgets import HiddenInput, MultipleHiddenInput
from django import forms
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


#class FlatPageAdmin(admin.ModelAdmin):
#    fields = ('title', 'content')


class PageForm(FlatpageForm):
    base_url = '/investigacion/faq/' # SETTINGS

    url = forms.CharField(label='', max_length=100, required=False)
    enable_comments = forms.BooleanField(label='', required=False)
    template_name = forms.CharField(label='', max_length=70, required=False)
    registration_required = forms.BooleanField(label='', required=False)
    sites = forms.ModelMultipleChoiceField(queryset=Site.objects.all(),
                                           required=False, label='')

    def __init__(self, *args, **kwargs):
        '''
            Fields: url, title, content, sites, enable_comments,
                    registration_required, template_name
        '''
        super(FlatpageForm, self).__init__(*args, **kwargs)
#        self.fields['url'].required = False
        self.fields['url'].initial = self.base_url
        self.fields['url'].widget = HiddenInput()
#        self.fields['sites'].required = False
        self.fields['sites'].widget = MultipleHiddenInput()
#        self.fields['enable_comments'].widget = HiddenInput()
#        self.fields['registration_required'].widget = HiddenInput()
#        self.fields['template_name'].widget = HiddenInput()

    def save(self, commit=True):
        flatpage = super(PageForm, self).save(commit=False)
        flatpage.save()
        flatpage.url = self.base_url + str(flatpage.id) + '/'
        flatpage.sites.add(Site.objects.all()[0])
        return flatpage

    class Meta:
        model = FlatPage
        widgets = {
            'content': TinyMCE(attrs={'cols': 100, 'rows': 15}),
        }


class PageAdmin(FlatPageAdmin):
    form = PageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
    )


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
