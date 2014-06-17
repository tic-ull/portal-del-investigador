# -*- encoding: UTF-8 -*-

from django.core.management.base import BaseCommand
from cvn.models import CVN


class Command(BaseCommand):
    help = u'Insertar todos los CVN'

    def handle(self, *args, **options):
        try:
            for cvn in CVN.objects.filter(is_inserted=False):
                cvn.remove_producciones()
                cvn.insert_xml()
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
