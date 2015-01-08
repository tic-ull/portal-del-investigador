# -*- encoding: UTF-8 -*-

from .models import CVN
from cvn import settings as st_cvn
from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.admin import widgets
from django.utils.translation import ugettext_lazy as _

import fecyt
import mimetypes


class UploadCVNForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.xml = None
        if 'instance' in kwargs and kwargs['instance'] is not None:
            self.user = kwargs['instance'].user_profile.user
        if 'data' in kwargs and 'user' in kwargs['data']:
            try:
                self.user = User.objects.get(pk=kwargs['data']['user'].pk)
            except:
                self.user = User.objects.get(pk=kwargs['data']['user'])
        if 'initial' in kwargs and 'cvn_file' in kwargs['initial']:
            if 'data' not in kwargs:
                kwargs['data'] = {}
            kwargs['data']['cvn_file'] = kwargs['initial']['cvn_file']
        super(UploadCVNForm, self).__init__(*args, **kwargs)

    def clean_cvn_file(self):
        try:
            cvn_file = self.cleaned_data['cvn_file']
        except:
            cvn_file = self.data['cvn_file']
        if mimetypes.guess_type(cvn_file.name)[0] != "application/pdf":
            raise forms.ValidationError(
                _(u'El CVN debe estar en formato PDF.'))
        cvn_file.open()
        (self.xml, error) = fecyt.pdf2xml(cvn_file.read(), cvn_file.name)
        if not self.xml:
            raise forms.ValidationError(_(st_cvn.ERROR_CODES[error]))
        return cvn_file

    @transaction.atomic
    def save(self, commit=True):
        CVN.remove_cvn_by_userprofile(self.user.profile)
        cvn = super(UploadCVNForm, self).save(commit=False)
        cvn.user_profile = self.user.profile
        cvn.update_fields(self.xml, commit)
        if commit:
            cvn.save()
        return cvn

    class Meta:
        model = CVN
        fields = ['cvn_file']


class GetDataCVNULL(forms.Form):
    year = forms.ChoiceField(widget=forms.Select(), required=False)
    start_year = forms.ChoiceField(widget=forms.Select(), required=False)
    end_year = forms.ChoiceField(widget=forms.Select(), required=False)

    def __init__(self, *args, **kwargs):
        super(GetDataCVNULL, self).__init__(*args, **kwargs)
        choices = [(x, x) for x in range(st_cvn.RANGE_OF_YEARS[0],
                                         st_cvn.RANGE_OF_YEARS[1])]
        self.fields['year'].choices = choices
        self.fields['start_year'].choices = choices
        self.fields['end_year'].choices = choices

    def clean_end_year(self):
        try:
            start_year = int(self.cleaned_data['start_year'])
            end_year = int(self.cleaned_data['end_year'])
            if end_year < start_year:
                raise forms.ValidationError(_("La fecha final no puede ser mayor "
                                          "que la inicial"))
        except ValueError:
            pass


