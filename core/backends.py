# -*- encoding: UTF-8 -*-

from django.contrib.auth.models import User
from django_cas.backends import _verify
import django_cas
import datetime
from core.models import Log
from core import settings as stCore


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
            # Add to User more info
            if 'first_name' in attributes:
                user.first_name = attributes['first_name']
            if 'last_name' in attributes:
                user.last_name = attributes['last_name']
            if 'email' in attributes:
                user.email = attributes['email']
            user.save()
        return user
