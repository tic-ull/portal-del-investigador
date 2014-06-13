# -*- encoding: UTF-8 -*-

#from cvn import settings as stCVN
from django.conf import settings as st
from django.core.management.base import BaseCommand
from statistics.models import Department
import json
import logging
import urllib

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        department_stats = []
        WS = '%sget_departamentos_y_miembros' % (st.WS_SERVER_URL)
        try:
            department_list = json.loads(urllib.urlopen(WS).read())
            Department.objects.create_all(department_list)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        # Update data shared in memory
        #print department_stats
        return department_stats  # Remove
