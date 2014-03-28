# -*- coding: utf-8 -*-
from cgi import escape
from django import forms
from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from cvn.models import CVN


class ShortNameClarableFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None):
        subs = {
            'initial_text': '',
            'input_text': '',
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }

        template = u'%(input)s'

        subs['input'] = super(ClearableFileInput, self)\
            .render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial

            # I just changed this line
            subs['initial'] = (u'<a href="%s" target>%s</a>'
                               % (escape(value.url),
                                  escape(force_unicode(''))))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                subs['clear_checkbox_name'] = conditional_escape(checkbox_name)
                subs['clear_checkbox_id'] = conditional_escape(checkbox_id)
                subs['clear'] = forms.CheckboxInput()\
                    .render(checkbox_name, False, attrs={'id': checkbox_id})
                subs['clear_template'] = self.template_with_clear % subs
        string = template % subs
        return mark_safe(string.replace(':', '').replace('<br />', ''))
        #return mark_safe(template % subs)


class UploadCvnForm(ModelForm):
    """
        Formulario que recoge un CVN en formato PDF e introduce
        sus datos en la BBDD de la aplicación CVN
    """
    class Meta:
        model = CVN
        widgets = {
            'cvn_file': ShortNameClarableFileInput,
        }
        fields = ('cvn_file',)   # 'investigador'
