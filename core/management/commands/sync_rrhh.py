# -*- encoding: UTF-8 -*-

from django.core.management.base import BaseCommand
from core.models import UserProfile


class Command(BaseCommand):
    help = u'Sync user rrhh code'

    def handle(self, *args, **options):
        for profile in UserProfile.objects.all():
            profile.update_rrhh_code()
