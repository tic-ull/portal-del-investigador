# -*- encoding: UTF-8 -*-

from django.core.management.base import BaseCommand
from statistics.models import Department
from statistics.settings import WS_ALL_DEPARTMENTS
import json
import logging
import urllib

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            department_list = json.loads(urllib.urlopen(
                                         WS_ALL_DEPARTMENTS).read())
            Department.objects.all().delete()
            Department.objects.create_all(department_list)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
