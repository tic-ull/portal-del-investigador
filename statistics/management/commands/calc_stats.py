# -*- encoding: UTF-8 -*-

from cvn.utils import isdigit
from core.ws_utils import CachedWS as ws
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from statistics.models import Department, ProfessionalCategory
from django.conf import settings as st
import logging

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

    def _check_args(self, options):
        if (not isdigit(options['past_days']) and
                options['past_days'] is not None):
            raise CommandError(
                'Option `--past_days=X` must be a number')

    def handle(self, *args,  **options):
        self._check_args(options)
        try:
            department_list = ws.get(ws=st.WS_ALL_DEPARTMENTS, use_redis=False)
            if department_list is None:
                raise IOError('WebService "%s" does not work' %
                              st.WS_ALL_DEPARTMENTS)
            Department.objects.all().delete()
            ProfessionalCategory.objects.update(options['past_days'])
            Department.objects.create_all(department_list)
        except Exception as e:
            raise type(e)(e.message)
