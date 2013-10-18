# -*- encoding: utf8 -*-
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = u'Encuentra registros sospechosos de estar duplicados'

    # constructor
    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
		raise NotImplementedError("Todavía no está hecho...")
        
