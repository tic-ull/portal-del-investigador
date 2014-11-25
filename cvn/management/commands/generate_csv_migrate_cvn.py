# -*- encoding: UTF-8 -*-

from cvn.models import CVN
from cvn.settings import MIGRATION_ROOT, PDF_ROOT
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import csv
import os
import shutil


class Command(BaseCommand):
    help = 'Generate CSV file to migrate users and their CVNs'

    option_list = BaseCommand.option_list + (
        make_option(
            "-d",
            "--date",
            dest="creation_date",
            help="Specify the creation date in format dd-mm-yyyy"
        ),
    )

    def check_args(self, options):
        if options['creation_date'] is None:
            raise CommandError(
                'Option --date="<dd-mm-yyyy>" must be specified.')
        try:
            creation_date = datetime.strptime(
                options['creation_date'], '%d-%m-%Y')
        except ValueError as e:
            raise CommandError(e)
        return creation_date

    def handle(self, *args, **options):
        creation_date = self.check_args(options)
        cvn_path = os.path.join(MIGRATION_ROOT, PDF_ROOT)
        if not os.path.isdir(cvn_path):
            os.makedirs(cvn_path)
        csv_file = csv.writer(
            open(os.path.join(MIGRATION_ROOT, 'users_to_migrate.csv'), 'wb'),
            delimiter=';')
        lines = 0
        for cvn in CVN.objects.filter(updated_at__gte=creation_date):
            lines += 1
            try:
                shutil.copyfile(
                    cvn.cvn_file.path, MIGRATION_ROOT + '/' + cvn.cvn_file.name)
                csv_file.writerow([
                    cvn.user_profile.user.username,
                    cvn.user_profile.documento,
                    cvn.cvn_file.name,
                    cvn.user_profile.user.first_name.upper().encode('utf8'),
                    cvn.user_profile.user.last_name.upper().encode('utf8')])
                print u'[%s] Usuario: %s - CVN: %s \t \t OK' % (
                    lines,
                    cvn.user_profile.user.username,
                    cvn.cvn_file.name)
            except Exception as e:
                print u'[%s] \t \t ERROR: Usuario no insertado (%s - %s)' % (
                    lines,
                    cvn.user_profile.user.username,
                    cvn.cvn_file.name)
                print e