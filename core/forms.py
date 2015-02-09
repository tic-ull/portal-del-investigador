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

from django import forms
from django.conf import settings as st
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.sites.models import Site
from django.forms.widgets import HiddenInput, MultipleHiddenInput


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
