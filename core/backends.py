# -*- encoding: UTF-8 -*-

from django.db import IntegrityError
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
        if not documento:
            Log.objects.create(
                user_profile=None,
                application='core',
                entry_type=stCore.LogType.AUTH_ERROR,
                date=datetime.datetime.now(),
                message='NumDocumento key not found at CAS. Username=' +
                        username)
            return None
        try:
            user = User.objects.get(profile__documento=documento)
        except User.DoesNotExist:
            try:
                # User will have an "unusable" password
                user = User.objects.create_user(username, '')
            except IntegrityError:
                Log.objects.create(
                    user_profile=None,
                    application='core',
                    entry_type=stCore.LogType.AUTH_ERROR,
                    date=datetime.datetime.now(),
                    message='Username already exists. Username=' + username +
                            ' New ID=' + documento)
                return None
            # Add to User more info
            if 'first_name' in attributes:
                user.first_name = attributes['first_name']
            if 'last_name' in attributes:
                user.last_name = attributes['last_name']
            if 'email' in attributes:
                user.email = attributes['email']
            user.save()
        return user
