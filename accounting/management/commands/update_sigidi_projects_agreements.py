# -*- encoding: UTF-8 -*-

from accounting.sigidi import SigidiConnection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = u'Actualiza la información de Proyectos' \
           u' y Convenios a partir de SIGIDI'

    def handle(self, *args, **options):
        sigidi = SigidiConnection()
        sigidi.update_projects()
        sigidi.update_convenios()









