# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import FECYT, CVN
from django import forms
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _


class UploadCVNForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        if 'instance' in kwargs and kwargs['instance'] is not None:
            self.user = kwargs['instance'].user_profile.user
        super(UploadCVNForm, self).__init__(*args, **kwargs)

    def clean_cvn_file(self):
        cvn_file = self.cleaned_data['cvn_file']
        if cvn_file.content_type != stCVN.PDF:
            raise forms.ValidationError(_("El CVN debe estar en formato PDF."))
        (self.xml, error) = FECYT.getXML(cvn_file)
        if not self.xml:
            raise forms.ValidationError(_(stCVN.ERROR_CODES[error]))
        if not CVN.can_user_upload_cvn(self.user, self.xml):
            raise forms.ValidationError(_(
                u'El NIF/NIE del CVN no coincide con el de su usuario.'))
        return cvn_file

    def save(self, commit=True):
        cvn = super(UploadCVNForm, self).save(commit=False)
        if self.user:
            cvn.cvn_file.name = u'CVN-%s.pdf' % (self.user.username)
        if self.user.profile.cvn:
            self.user.profile.cvn.remove()
        if commit:
            cvn.fecha_cvn = CVN.getXMLDate(self.xml)
            cvn.xml_file.save(cvn.cvn_file.name.replace('pdf', 'xml'),
                              ContentFile(self.xml))
            self.user.profile.cvn = cvn
            self.user.profile.save()
            self.user.profile.cvn.insertXML(self.user.profile)
        return cvn

    class Meta:
        model = CVN
        fields = ['cvn_file']
