# -*- encoding: UTF-8 -*-

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from cvn import settings as st_cvn
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

    def handle(self, *args, **options):
        list_cvn = os.listdir(st_cvn.OLD_PDF_ROOT)
        for cvn in list_cvn:
            username = cvn.split('-')[1]
            search_dict = {'username': username}
            user = self.get_user(search_dict)
            # Search for DNI in username and field "documento" in profile
            if not user and username[:-1].isdigit() and username[-1].isalpha():
                search_dict['username'] = username[:-1]
                user = self.get_user(search_dict)
                if not user:
                    user = self.get_user({
                        'profile__documento__iexact': username})
            if user:
                file_path = st_cvn.OLD_PDF_ROOT + cvn
                OldCvnPdf(user_profile=user.profile,
                          cvn_file=SimpleUploadedFile(cvn,
                                                      open(file_path).read(),
                                                      content_type=st_cvn.PDF),
                          uploaded_at=datetime.datetime.now()).save()
                os.remove(file_path)
            else:
                print '%s (%s) not found' % (username, cvn)