# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from cvn.models import FECYT, CVN
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from lxml import etree
from parser_helpers import parse_date


class UploadCVNForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        if 'instance' in kwargs and kwargs['instance'] is not None:
            self.user = kwargs['instance'].user_profile.user
        if 'data' in kwargs and 'user' in kwargs['data']:
            self.user = User.objects.get(pk=kwargs['data']['user'])
        super(UploadCVNForm, self).__init__(*args, **kwargs)

    def clean_cvn_file(self):
        cvn_file = self.cleaned_data['cvn_file']
        if cvn_file.content_type != stCVN.PDF:
            raise forms.ValidationError(_("El CVN debe estar en formato PDF."))
        (self.xml, error) = FECYT.getXML(cvn_file)
        if not self.xml:
            raise forms.ValidationError(_(stCVN.ERROR_CODES[error]))
        '''
        if not self.user.profile.can_upload_cvn(self.xml):
            raise forms.ValidationError(_(
                u'El NIF/NIE del CVN no coincide con el de su usuario.'))
        '''
        return cvn_file

    def save(self, commit=True):
        cvn = super(UploadCVNForm, self).save(commit=False)
        try:
            cvn_old = CVN.objects.get(user_profile=self.user)
            cvn_old.remove()
            cvn_old.delete()
        except ObjectDoesNotExist:
            pass
        cvn.cvn_file.name = u'CVN-%s.pdf' % (self.user.username)
        cvn.user_profile = self.user.profile
        cvn.xml_file.save(cvn.cvn_file.name.replace('pdf', 'xml'),
                          ContentFile(self.xml), save=False)
        treeXML = etree.XML(self.xml)
        cvn.fecha_cvn = parse_date(treeXML.find('Version/VersionID/Date'))
        cvn.update_status()
        cvn.save()
        cvn.insert_xml()
        return cvn

    class Meta:
        model = CVN
        fields = ['cvn_file']
