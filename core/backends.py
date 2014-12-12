# -*- encoding: UTF-8 -*-

from django.conf import settings as st
from django_cas.backends import _verify
import django_cas
from core.models import UserProfile


class CASBackend(django_cas.backends.CASBackend):

    def authenticate(self, ticket, service, request):
        username, attributes = _verify(ticket, service)
        # If we don't have the users document we dont allow to login
        if (not attributes or not 'NumDocumento' in attributes
                or not attributes['NumDocumento']):
            st.CAS_RETRY_LOGIN = False
            return None
        # If the account should not be allowed to login we dont log in the user
        if attributes and 'TipoCuenta' in attributes:
            if attributes['TipoCuenta'] in st.CAS_TIPO_CUENTA_NOAUT:
                st.CAS_RETRY_LOGIN = False
                return None
        documento = attributes['NumDocumento']
        user = UserProfile.get_or_create_user(username, documento)[1]
        return user