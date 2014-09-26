# -*- encoding: UTF-8 -*-

from django.core.management.base import BaseCommand
from cvn.models import CVN


class Command(BaseCommand):
    help = u'Actualiza el estado de todos los CVN'

    def handle(self, *args, **options):
        list_email = []
        for cvn in CVN.objects.all():
            try:
                email = cvn.update_status()
                if email:
                    list_email.append(str(email))
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))
        print list_email

    def send_mail_from_template(self, list_email):


