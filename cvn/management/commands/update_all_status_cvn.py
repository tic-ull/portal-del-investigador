# -*- encoding: UTF-8 -*-

from cvn.models import CVN
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = u'Actualiza el estado de todos los CVN'

    def handle(self, *args, **options):
        for cvn in CVN.objects.all():
            try:
                cvn.update_status()
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))

