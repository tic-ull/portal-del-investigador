# -*- encoding: UTF-8 -*-

from django.core.management.base import BaseCommand
from cvn.models import CVN


class Command(BaseCommand):
    help = u'Actualiza el estado de todos los CVN'

    def handle(self, *args, **options):
        [cvn.update_status() for cvn in CVN.objects.all()]
