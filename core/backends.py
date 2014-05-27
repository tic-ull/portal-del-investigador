# -*- encoding: UTF-8 -*-

from core import settings as stCore
from core.models import Log
from django.contrib.auth.models import User
from django_cas.backends import _verify
import datetime
import django_cas


class CASBackend(django_cas.backends.CASBackend):

    def authenticate(self, ticket, service, request):
        """Verifies CAS ticket and gets or creates User object"""
        username, attributes = _verify(ticket, service)
        documento = None
        if attributes and 'NumDocumento' in attributes:
            request.session['attributes'] = attributes
            documento = attributes['NumDocumento']
        try:
            user = User.objects.get(profile__documento=documento)
        except User.DoesNotExist:
            user, created = User.objects.get_or_create(username=username)
            if not created:
                Log.objects.create(
                    user_profile=user.profile,
                    application='core',
                    entry_type=stCore.LogType.AUTH_ERROR,
                    date=datetime.datetime.now(),
                    message='Username already exists. Possibly changed ID.' +
                            ' Old ID=' + user.profile.documento +
                            ' New ID=' + documento)
        return user
