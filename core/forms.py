# -*- encoding: UTF-8 -*-

from django import forms
from django.conf import settings as st
from django.contrib.sites.models import Site
from django.forms.widgets import HiddenInput, MultipleHiddenInput
from django.contrib.flatpages.forms import FlatpageForm
import settings as st_core


class PageForm(FlatpageForm):

    url = forms.CharField(label='', max_length=100, required=False)

    sites = forms.ModelMultipleChoiceField(queryset=Site.objects.all(),
                                           required=False, label='')

    template_name = forms.CharField(label='', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(FlatpageForm, self).__init__(*args, **kwargs)
        self.fields['url'].initial = ''
        self.fields['url'].widget = HiddenInput()
        self.fields['template_name'].widget = HiddenInput()
        self.fields['sites'].widget = MultipleHiddenInput()
        content_field = 'content_' + st.LANGUAGE_CODE
        self.fields[content_field].required = True

    def clean_url(self):
        return True

    def save(self, commit=True):
        flatpage = super(PageForm, self).save(commit=False)
        flatpage.save()
        flatpage.url = '/' + str(flatpage.id) + '/'
        flatpage.template_name = 'core/faq/question_faq.html'
        flatpage.sites.add(Site.objects.get(id=st.SITE_ID))
        return flatpage

    class Meta:
        widgets = {
            'content': forms.widgets.Textarea(),
        }

    class Media:
        js = (st.TINYMCE_JS_URL, st.TINYMCE_JS_TEXTAREA)
