# -*- encoding: UTF-8 -*-

from core.models import UserProfile
from cvn import settings as stCVN
from cvn.forms import UploadCVNForm
from django.conf import settings as st
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
import csv
import os


class Command(BaseCommand):
    help = u'Migración de usuarios con su CVN desde un CSV del viejo portal'

    def handle(self, *args,  **options):
        import_path = os.path.join(st.BASE_DIR, 'importCVN/')
        csv_file = import_path + 'users_to_migrate.csv'
        with open(csv_file, 'rb') as csvfile:
            lines = csv.reader(csvfile, delimiter=';')
            for line in lines:
                print u'Línea: %s' % (lines.line_num)
                print u'Usuario: %s' % (line[0])
                print u'CVN: %s' % (line[2])
                user = User.objects.get_or_create(
                    username=unicode(line[0]), password='')[0]
                UserProfile.objects.get_or_create(user=user)[0]
                user.profile.documento = unicode(line[1])
                user.profile.save()
                try:
                    upload_file = open(import_path + line[2], 'r')
                except IOError:
                    print u'ERROR: CVN No encontrado (%s - %s)' % (
                        line[0], line[2])
                    print u'----------------------------------------'
                    continue
                cvn_file = SimpleUploadedFile(
                    upload_file.name,
                    upload_file.read(),
                    content_type=stCVN.PDF)
                form = UploadCVNForm(initial={'cvn_file': cvn_file}, user=user)
                if form.is_valid():
                    form.save()
                    print u'OK'
                else:
                    print u'ERROR: CVN No válido (%s - %s)' % (
                        line[0], line[2])
                print u'----------------------------------------'
