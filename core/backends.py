# -*- encoding: UTF-8 -*-

import django_cas
from django_cas.backends import _verify
from django.contrib.auth.models import User


class CASBackend(django_cas.backends.CASBackend):
    def authenticate(self, ticket, service, request):
        """Verifies CAS ticket and gets or creates User object"""

        username, attributes = _verify(ticket, service)
        if attributes and 'mail' in attributes:
            # correos ULL (original y alias) nos quedamos con el principal
            try:
                attributes['real_email'] = filter(
                    lambda x: x.startswith(username + "@"),
                    attributes['mail']).pop()
            except IndexError:
                attributes['real_email'] = attributes['mail']
            except AttributeError:
                attributes['real_email'] = attributes['mail']
        request.session['attributes'] = attributes or {}
        documento = None
        if 'NumDocumento' in attributes:
            documento = attributes['NumDocumento']
        if not documento:
            return None
        try:
            user = User.objects.get(profile__documento=documento)
        except User.DoesNotExist:
            # user will have an "unusable" password
            user = User.objects.create_user(username, '')
            ## Add to User more datas
            user.first_name = attributes.get('first_name', '')[:30]
            user.last_name = attributes.get('last_name', '')[:30]
            user.email = attributes.get('real_email', '')
            user.save()
        return user
