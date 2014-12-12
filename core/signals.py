# -*- encoding: UTF-8 -*-

from crequest.middleware import CrequestMiddleware
from django.contrib.auth.signals import user_logged_in
from statistics.models import Department


def update_personal_data(request, user):
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


def send_department(request, user):
    if request:
        (dept, dept_json) = Department.get_user_department(
            user.profile.rrhh_code)
        if dept is not None and dept_json is not None:
            request.session['dept'] = dept.name
            request.session['dept_json'] = dept_json


def update_profile(user, **kwargs):
    request = CrequestMiddleware.get_request()
    update_personal_data(request, user)
    send_department(request, user)

user_logged_in.connect(update_profile, dispatch_uid='update-profile')
