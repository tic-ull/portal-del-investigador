# -*- encoding: UTF-8 -*-

from django.contrib.auth.models import User
from django.conf import settings as st
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.move import file_move_safe
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from cvn import settings as st_cvn
from cvn.helpers import get_cvn_path
from cvn.models import OldCvnPdf

import datetime
import os


class Command(BaseCommand):
    help = u'Assigna al usuario los antiguos CVNs como historicos '

    def get_user(self, search_dict={}):
        try:
            user = User.objects.get(**search_dict)
        except ObjectDoesNotExist:
            user = None
        return user

    def cvn2user(self, user, cvn):
        file_path = st_cvn.OLD_PDF_ROOT + cvn
        old_cvn = OldCvnPdf(user_profile=user.profile,
                            cvn_file=SimpleUploadedFile(
                                cvn,
                                open(file_path).read(),
                                content_type=st_cvn.PDF),
                            uploaded_at=datetime.datetime.now())
        os.remove(file_path)
        filename = 'CVN-%s' % user.profile.documento
        for data in cvn.split('-')[2:]:
            filename += '-%s' % data
        old_cvn.cvn_file.name = st_cvn.OLD_PDF_ROOT + filename
        old_cvn.save()

    def relocate_old_cvn(self):
        for cvn in OldCvnPdf.objects.all():
            filename = 'old/%s' % cvn.cvn_file.name.split('/')[-1]
            new_name = get_cvn_path(cvn, filename)
            path = os.path.join(st.MEDIA_ROOT, new_name)

            root_dir = '/'.join(path.split('/')[:-1])
            if not os.path.isdir(root_dir):
                os.makedirs(root_dir)

            file_move_safe(cvn.cvn_file.path, path, allow_overwrite=True)
            cvn.cvn_file.name = new_name
            cvn.save()

    def handle(self, *args, **options):
        list_cvn = os.listdir(st_cvn.OLD_PDF_ROOT)
        for cvn in list_cvn:
            username = cvn.split('-')[1]
            search_dict = {'username': username}
            user = self.get_user(search_dict)
            # Search for DNI in "username" field
            if not user and username[:-1].isdigit() and username[-1].isalpha():
                search_dict['username'] = username[:-1]
                user = self.get_user(search_dict)
            # Search  "document" field in the table "profile"
            if not user:
                user = self.get_user({'profile__documento__iexact': username})
            if user:
                self.cvn2user(user, cvn)
            else:
                print '%s (%s) not found' % (username, cvn)
        self.relocate_old_cvn()
