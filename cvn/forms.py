# -*- encoding: UTF-8 -*-

from cvn.models import CVN
from django.forms import ModelForm


class UploadCVNForm(ModelForm):

    class Meta:
        model = CVN
        fields = ['cvn_file']
