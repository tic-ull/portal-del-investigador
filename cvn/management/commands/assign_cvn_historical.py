# -*- encoding: UTF-8 -*-

from django.contrib.auth.models import User
from django.conf import settings as st
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.move import file_move_safe
from django.core.management.base import BaseCommand
from cvn import settings as st_cvn
from cvn.fecyt import pdf2xml
from cvn.helpers import get_cvn_path
from cvn.parsers.read_helpers import parse_nif
from cvn.models import OldCvnPdf
from lxml import etree


import datetime
import os


class Command(BaseCommand):
    help = u'Assigna al usuario los antiguos CVNs como historicos '
    is_documento = lambda self, username: username[1:-1].isdigit() and \
                                          username[-1].isalpha()

    def get_user(self, search_dict={}):
        try:
            user = User.objects.get(**search_dict)
        except ObjectDoesNotExist:
            user = None
        return user

    def cvn2user(self, user, cvn):
        filename = 'old/CVN-%s' % user.profile.documento
        for data in cvn.split('-')[2:]:
            filename += '-%s' % data
        old_file_path = os.path.join(st_cvn.OLD_PDF_ROOT, cvn)
        file_path = os.path.join(st_cvn.OLD_PDF_ROOT, filename.split('/')[-1])
        os.rename(old_file_path, file_path)
        # The object is created to calculate the new path
        old_cvn = OldCvnPdf(user_profile=user.profile,
                            cvn_file=None,
                            uploaded_at=datetime.datetime.now())
        # Relocate old cvn
        old_cvn_path = get_cvn_path(old_cvn, filename)
        old_cvn_new_path = os.path.join(st.MEDIA_ROOT, old_cvn_path)
        root_dir = '/'.join(old_cvn_new_path.split('/')[:-1])
        if not os.path.isdir(root_dir):
            os.makedirs(root_dir)
        file_move_safe(file_path, old_cvn_new_path, allow_overwrite=True)
        # The resulting file from the object creation is deleted
        old_cvn.cvn_file.name = old_cvn_path
        old_cvn.save()

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