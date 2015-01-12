# -*- encoding: UTF-8 -*-

from crequest.middleware import CrequestMiddleware
from django.contrib.auth.signals import user_logged_in
from statistics.models import Department, Area


def send_department(request, user):
    if request:
        (dept, dept_json) = Department.get_user_unit(
            rrhh_code=user.profile.rrhh_code)
        if dept is not None and dept_json is not None:
            request.session['dept'] = dept.name
            request.session['dept_json'] = dept_json


def send_area(request, user):
    if request:
        (area, area_json) = Area.get_user_unit(
            rrhh_code=user.profile.rrhh_code)
        if area is not None and area_json is not None:
            request.session['area'] = area.name
            request.session['area_json'] = area_json


def info_to_session(user, **kwargs):
    request = CrequestMiddleware.get_request()
    send_department(request, user)
    send_area(request, user)

user_logged_in.connect(info_to_session, dispatch_uid='info_to_session')