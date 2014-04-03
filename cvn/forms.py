# -*- encoding: UTF-8 -*-

from cvn.models import CVN
from django import forms
from cvn import settings as stCVN


class UploadCVNForm(forms.ModelForm):

    def clean_cvn_file(self):
        fileCVN = self.cleaned_data['cvn_file']
        if fileCVN.content_type != stCVN.PDF:
            raise forms.ValidationError("El CVN debe estar en formato PDF.")
        else:
            return fileCVN

    class Meta:
        model = CVN
        fields = ['cvn_file']
