# -*- encoding: UTF-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from lxml import etree
from models import FECYT, CVN
from parser_helpers import parse_date
import settings as st_cvn


class UploadCVNForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
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
        if cvn_file.content_type != st_cvn.PDF:
            raise forms.ValidationError(
                _(u'El CVN debe estar en formato PDF.'))
        (self.xml, error) = FECYT.pdf2xml(cvn_file)
        if not self.xml:
            raise forms.ValidationError(_(st_cvn.ERROR_CODES[error]))
        return cvn_file

    @transaction.atomic
    def save(self, commit=True):
        CVN.remove_pdf_by_userprofile(self.user.profile)
        cvn = super(UploadCVNForm, self).save(commit=False)
        cvn.update_fields(self.user, self.xml)
        if commit:
            cvn.save()
        return cvn

    @staticmethod
    def CVN(user, pdf_path):
        upload_file = open(pdf_path)
        cvn_file = SimpleUploadedFile(
            upload_file.name, upload_file.read(), content_type=st_cvn.PDF)
        upload_file.close()
        try:
            cvn = CVN.objects.get(user_profile__user=user)
        except ObjectDoesNotExist:
            cvn = None
        form = UploadCVNForm(initial={'cvn_file': cvn_file},
                             user=user, instance=cvn)
        if form.is_valid():
            cvn = form.save()
        return cvn

    class Meta:
        model = CVN
        fields = ['cvn_file']
