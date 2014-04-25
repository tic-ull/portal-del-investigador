# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import FECYT, CVN
from lxml import etree
from django import forms
from parser_helpers import parse_date
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _


class UploadCVNForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UploadCVNForm, self).__init__(*args, **kwargs)

    def clean_cvn_file(self):
        cvn_file = self.cleaned_data['cvn_file']
        if cvn_file.content_type != stCVN.PDF:
            raise forms.ValidationError(_("El CVN debe estar en formato PDF."))
        (self.xml, error) = FECYT.getXML(cvn_file)
        if not self.xml:
            raise forms.ValidationError(_(stCVN.ERROR_CODES[error]))
        if not self.user.profile.can_upload_cvn(self.xml):
            raise forms.ValidationError(_(
                u'El NIF/NIE del CVN no coincide con el de su usuario.'))
        return cvn_file

    def save(self, commit=True):
        cvn = super(UploadCVNForm, self).save(commit=False)
        if self.user and self.user.username:
            cvn.cvn_file.name = u'CVN-%s.pdf' % (self.user.username)
        if self.xml:
            cvn.xml_file.save(cvn.cvn_file.name.replace('pdf', 'xml'),
                              ContentFile(self.xml), save=False)
            treeXML = etree.XML(self.xml)
            cvn.fecha_cvn = parse_date(treeXML)
        if commit:
            if self.user.profile.cvn:
                self.user.profile.cvn.remove()
            cvn.save()
            self.user.profile.cvn = cvn
            self.user.profile.save()
            self.user.profile.cvn.insert_xml()
        return cvn

    class Meta:
        model = CVN
        fields = ['cvn_file']
