# -*- encoding: UTF-8 -*-

from core import settings as stCore
from django import forms
from django.conf import settings as st
from django.contrib.flatpages.admin import FlatpageForm
from django.contrib.flatpages.models import Site, FlatPage
from django.forms.widgets import HiddenInput, MultipleHiddenInput
from tinymce.widgets import TinyMCE


class PageForm(FlatpageForm):

    url = forms.CharField(label='', max_length=100, required=False)
    sites = forms.ModelMultipleChoiceField(queryset=Site.objects.all(),
                                           required=False, label='')

    def __init__(self, *args, **kwargs):
        super(FlatpageForm, self).__init__(*args, **kwargs)
        self.fields['url'].initial = stCore.BASE_URL_FLATPAGES
        self.fields['url'].widget = HiddenInput()
        self.fields['sites'].widget = MultipleHiddenInput()

    def clean_url(self):
        return True

    def save(self, commit=True):
        flatpage = super(PageForm, self).save(commit=False)
        flatpage.save()
        flatpage.url = stCore.BASE_URL_FLATPAGES + str(flatpage.id) + '/'
        flatpage.sites.add(Site.objects.get(id=st.SITE_ID))
        return flatpage

    class Meta:
        model = FlatPage
        widgets = {
            'content': TinyMCE(attrs={'cols': 100, 'rows': 15}),
        }
