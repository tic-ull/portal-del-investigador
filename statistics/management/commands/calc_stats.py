# -*- encoding: UTF-8 -*-

from cvn.utils import isdigit
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from statistics.models import Department, ProfessionalCategory
from statistics.settings import WS_ALL_DEPARTMENTS
import json
import logging
import urllib

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = u'Calcula las estadísticas de los departamentos y actualiza las\
            categorías profesionales'
    option_list = BaseCommand.option_list + (
        make_option(
            '-d',
            '--past_days',
            dest='past_days',
            default='0',
            help='Specify the days to update professional category',
        ),
    )

    def _checkArgs(self, options):
        if (not isdigit(options['past_days']) and
                options['past_days'] is not None):
            raise CommandError(
                'Option `--past_days=X` must be a number')

    def handle(self, *args, **options):
        self._checkArgs(options)
        try:
            department_list = json.loads(urllib.urlopen(
                                         WS_ALL_DEPARTMENTS).read())
            Department.objects.all().delete()
            ProfessionalCategory.objects.update(options['past_days'])
            Department.objects.create_all(department_list)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
