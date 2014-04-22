# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import CVN
from django import forms
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
import datetime


class UploadCVNForm(forms.ModelForm):

    def clean_cvn_file(self):
        fileCVN = self.cleaned_data['cvn_file']
        if fileCVN.content_type != stCVN.PDF:
            raise forms.ValidationError(_("El CVN debe estar en formato PDF."))
        else:
            return fileCVN

    def save(self, user=None, xml=None, commit=True):
        cvn = super(UploadCVNForm, self).save(commit=False)
        cvn.fecha_up = datetime.date.today()
        if user and user.username:
            cvn.cvn_file.name = u'CVN-%s.pdf' % (user.username)
        if xml:
            cvn.xml_file.save(cvn.cvn_file.name.replace('pdf', 'xml'),
                              ContentFile(xml), save=False)
            cvn.fecha_cvn = CVN.get_date_from_xml(xml)
        if commit:
            cvn.save()
        return cvn

    class Meta:
        model = CVN
        fields = ['cvn_file']
