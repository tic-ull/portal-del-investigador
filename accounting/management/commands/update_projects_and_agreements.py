# -*- encoding: UTF-8 -*-

from accounting.sigidi import SigidiConnection
from accounting.models import Project, Agreement
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = u'Actualiza la información de Proyectos y Convenios desde SIGIDI'

    def handle(self, *args, **options):
        try:
            sigidi = SigidiConnection()
            sigidi.update_entities(Project, Agreement)
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
