# -*- encoding: UTF-8 -*-

from django.conf import settings as st
from django_cas.backends import _verify
import django_cas
from core.models import UserProfile


class CASBackend(django_cas.backends.CASBackend):

    def authenticate(self, ticket, service, request):
        """Verifies CAS ticket and gets or creates User object"""
        username, attributes = _verify(ticket, service)
        # If we don't have the user's document we'll not allow him to do login
        if (not attributes or not 'NumDocumento' in attributes
                or attributes['NumDocumento'] is None):
            st.CAS_RETRY_LOGIN = False
            return None
        # If type of account of the user isn't allow then
        # we will not allow him to do login
        if (attributes and 'TipoCuenta' in attributes
                and attributes['TipoCuenta'] in st.CAS_TIPO_CUENTA_NOAUT):
            st.CAS_RETRY_LOGIN = False
            return None
        request.session['attributes'] = attributes
        documento = attributes['NumDocumento']
        return UserProfile.get_or_create_user(username, documento)[0]
