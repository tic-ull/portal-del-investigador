# -*- encoding: UTF-8 -*-

from cvn import settings as st_cvn
from cvn.models import CVN
from django.conf import settings as st
from django.core.files.move import file_move_safe
from django.core.management.base import BaseCommand

import os


class Command(BaseCommand):
    help = u'Reorganiza la hubicación de los CVN-PDF'

    def handle(self, *args, **options):
        for cvn in CVN.objects.all():
            try:
                pdf_name = u'%s/CVN-%s.pdf' % (
                    st_cvn.PDF_ROOT, cvn.user_profile.documento)
                new_pdf_path = os.path.join(
                    st.MEDIA_ROOT, pdf_name)
                if cvn.cvn_file.path != new_pdf_path:
                    file_move_safe(
                        cvn.cvn_file.path, new_pdf_path, allow_overwrite=True)
                    cvn.cvn_file.name = pdf_name

                xml_name = u'%s/CVN-%s.xml' % (
                    st_cvn.XML_ROOT, cvn.user_profile.documento)
                new_xml_path = os.path.join(
                    st.MEDIA_ROOT, xml_name)
                if cvn.xml_file.path != new_xml_path:
                    file_move_safe(
                        cvn.xml_file.path, new_xml_path, allow_overwrite=True)
                    cvn.xml_file.name = xml_name

                cvn.save()

            except Exception as e:
                print 'User: %s - CVN: %s' % (
                    cvn.user_profile.user, cvn.cvn_file)
                print '%s (%s)' % (e.message, type(e))
