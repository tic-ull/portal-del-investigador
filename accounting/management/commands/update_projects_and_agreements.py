# -*- encoding: UTF-8 -*-

from accounting.sigidi import SigidiConnection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = u'Actualiza la información de Proyectos y Convenios desde SIGIDI'

    def handle(self, *args, **options):
        try:
            sigidi = SigidiConnection()
            sigidi.update_projects()
            sigidi.update_agreements()
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))