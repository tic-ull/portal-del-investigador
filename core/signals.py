# -*- encoding: UTF-8 -*-

from crequest.middleware import CrequestMiddleware
from core.models import UserProfile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in


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


def update_profile(user, **kwargs):
    request = CrequestMiddleware.get_request()
    if request and 'attributes' in request.session:
        cas_info = request.session['attributes']
        if 'first_name' in cas_info:
            user.first_name = cas_info['first_name']
        if 'last_name' in cas_info:
            user.last_name = cas_info['last_name']
        if 'email' in cas_info:
            user.email = cas_info['email']
    user.save()

user_logged_in.connect(update_profile, dispatch_uid='update-profile')
