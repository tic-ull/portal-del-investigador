# -*- encoding: UTF-8 -*-

from crequest.middleware import CrequestMiddleware
from core.models import UserProfile
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def create_profile(sender, instance, created, **kwargs):
    if not created:
        return
    profile = UserProfile.objects.create(user=instance)
    request = CrequestMiddleware.get_request()
    if request and 'attributes' in request.session:
        cas_info = request.session['attributes']
        if 'NumDocumento' in cas_info:
            profile.documento = cas_info['NumDocumento']
            profile.update_rrhh_code()
    profile.save()

post_save.connect(create_profile, sender=User, dispatch_uid="create-profile")
