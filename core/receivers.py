# -*- encoding: UTF-8 -*-

from crequest.middleware import CrequestMiddleware
from django.contrib.auth.signals import user_logged_in


def update_user(user, **kwargs):
    request = CrequestMiddleware.get_request()
    if request and 'attributes' in request.session:
        cas_info = request.session['attributes']
        if 'first_name' in cas_info:
            user.first_name = cas_info['first_name']
        if 'last_name' in cas_info:
            user.last_name = cas_info['last_name'][:30]
        if 'email' in cas_info:
            user.email = cas_info['email']
        if 'username' in cas_info:
            user.username = cas_info['username']
        user.save()

user_logged_in.connect(update_user, dispatch_uid='update-profile')
