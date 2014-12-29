# -*- encoding: UTF-8 -*-

from cvn.fecyt import pdf2xml
from cvn.models import OldCvnPdf
from cvn.parsers.read_helpers import parse_nif
from django.conf import settings as st
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from django.db.models import Q
from lxml import etree

import datetime
import os


class Command(BaseCommand):
    help = u'Asigna a los usuarios sus antiguos CVNs'

    OLD_PDF_ROOT = os.path.join(st.MEDIA_ROOT, 'cvn/old_cvn/')

    def handle(self, *args, **options):
        for cvn in os.listdir(self.OLD_PDF_ROOT):
            username = cvn.split('-')[1]
            user = None
            try:
                user = User.objects.get(
                    Q(username=username) | Q(profile__documento=username))
            except ObjectDoesNotExist:
                cvn_file = open(os.path.join(self.OLD_PDF_ROOT, cvn))
                (xml, error) = pdf2xml(cvn_file)
                tree_xml = etree.XML(xml)
                documento = parse_nif(tree_xml)
                try:
                    user = User.objects.get(
                        profile__documento__iexact=documento)
                except ObjectDoesNotExist:
                    print '%s (%s) not found' % (username, cvn)

            if user is not None:
                self.cvn2user(cvn, user)

    def cvn2user(self, cvn, user):
        filename = 'CVN-%s-%s' % (
            user.profile.documento, '-'.join(cvn.split('-')[2:]))
        cvn_pdf_path = os.path.join(self.OLD_PDF_ROOT, cvn)
        cvn_pdf = open(cvn_pdf_path)
        old_cvn_file = SimpleUploadedFile(
            filename, cvn_pdf.read(), content_type="application/pdf")
        cvn_old = OldCvnPdf(
            user_profile=user.profile, cvn_file=old_cvn_file,
            uploaded_at=datetime.datetime.strptime(
                ','.join(cvn.replace('.pdf', '').split('-')[2:]), '%Y,%m,%d'))
        cvn_old.save()
        os.remove(cvn_pdf_path)
