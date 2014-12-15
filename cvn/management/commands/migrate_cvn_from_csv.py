# -*- encoding: UTF-8 -*-

from core.models import UserProfile
from cvn import settings as st_cvn
from cvn.forms import UploadCVNForm
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import csv
import os


class Command(BaseCommand):
    help = u'Migración de usuarios con su CVN desde un CSV del viejo portal'

    def handle(self, *args,  **options):
        cvn_file = os.path.join(st_cvn.MIGRATION_ROOT, 'users_to_migrate.csv')
        with open(cvn_file, 'rb') as csvfile:
            lines = csv.reader(csvfile, delimiter=';')
            for line in lines:
                user, created = UserProfile.get_or_create_user(
                    username=unicode(line[0]), documento=unicode(line[1]))
                if created:
                    user.first_name = line[3].decode('utf-8')
                    user.last_name = line[4].decode('utf-8')
                    user.save()

                # Reload user to have profile updated
                user = User.objects.get(pk=user.profile.user.pk)
                try:
                    pdf_file = os.path.join(st_cvn.MIGRATION_ROOT, line[2])
                    upload_file = open(pdf_file)
                except IOError:
                    print u'[%s] \t \t ERROR: CVN No encontrado (%s - %s)' % (
                        lines.line_num, line[0], line[2])
                    continue
                cvn_file = SimpleUploadedFile(
                    upload_file.name,
                    upload_file.read(),
                    content_type=st_cvn.PDF)
                upload_file.close()
                try:
                    user.profile.cvn.remove()
                    user.profile.cvn.delete()
                except ObjectDoesNotExist:
                    pass
                form = UploadCVNForm(initial={'cvn_file': cvn_file}, user=user)
                if form.is_valid():
                    cvn = form.save()
                    cvn.insert_xml()
                    print u'[%s] Usuario: %s - CVN: %s \t \t OK' % (
                        lines.line_num, line[0], line[2])
                else:
                    print u'[%s] \t \t ERROR: CVN No válido (%s - %s)' % (
                        lines.line_num, line[0], line[2])
