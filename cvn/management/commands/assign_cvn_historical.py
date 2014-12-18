# -*- encoding: UTF-8 -*-

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from cvn import settings as st_cvn
from cvn.fecyt import pdf2xml
from cvn.parsers.read_helpers import parse_nif
from cvn.models import OldCvnPdf
from lxml import etree


import datetime
import os


class Command(BaseCommand):
    help = u'Assigna al usuario los antiguos CVNs como historicos '
    is_documento = lambda self, username: username[1:-1].isdigit() and \
                                          username[-1].isalpha()

    def get_user(self, search_dict):
        try:
            user = User.objects.get(**search_dict)
        except ObjectDoesNotExist:
            user = None
        return user

    def cvn2user(self, user, cvn):
        filename = 'CVN-%s' % user.profile.documento
        for data in cvn.split('-')[2:]:
            filename += '-%s' % data
        cvn_file = open(os.path.join(st_cvn.OLD_PDF_ROOT, cvn))
        old_cvn_file = SimpleUploadedFile(
            filename, cvn_file.read(), content_type=st_cvn.PDF)
        cvn_old = OldCvnPdf(
            user_profile=user.profile, cvn_file=old_cvn_file,
            uploaded_at=datetime.datetime.now())
        cvn_old.save()

    def search_user(self, username, cvn):
        search_dict = dict()
        # Search by username
        if not self.is_documento(username):
            search_dict = {'username': username}
            user = self.get_user(search_dict)
        else:
        # Search by NIF/NIE in fields "username" and "documento" (UserProfile)
            search_dict['username__icontains'] = username[:-1]
            user = self.get_user(search_dict)
            if not user:
                user = self.get_user({'profile__documento__iexact': username})
        if not user:
            # Search in cvn file
            cvn_file_path = os.path.join(st_cvn.OLD_PDF_ROOT, cvn)
            cvn_file = open(cvn_file_path)
            (xml, error) = pdf2xml(cvn_file)
            tree_xml = etree.XML(xml)
            document = parse_nif(tree_xml)
            user = self.get_user({'profile__documento__iexact': document})
        return user

    def handle(self, *args, **options):
        list_cvn = os.listdir(st_cvn.OLD_PDF_ROOT)
        for cvn in list_cvn:
            username = cvn.split('-')[1]
            user = self.search_user(username, cvn)
            if user:
                self.cvn2user(user, cvn)
            else:
                print '%s (%s) not found' % (username, cvn)