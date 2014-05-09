# -*- encoding: UTF-8 -*-

from django.contrib.auth.models import User
from django_cas.backends import _verify
import django_cas


class CASBackend(django_cas.backends.CASBackend):

    def authenticate(self, ticket, service, request):
        """Verifies CAS ticket and gets or creates User object"""
        username, attributes = _verify(ticket, service)
        documento = None
        if attributes and 'NumDocumento' in attributes:
            request.session['attributes'] = attributes
            documento = attributes['NumDocumento']
        if not documento:
            return None
        try:
            user = User.objects.get(profile__documento=documento)
        except User.DoesNotExist:
            # User will have an "unusable" password
            user = User.objects.create_user(username, '')
        return user
