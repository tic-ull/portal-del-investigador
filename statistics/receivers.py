# -*- encoding: UTF-8 -*-

from crequest.middleware import CrequestMiddleware
from django.contrib.auth.signals import user_logged_in
from statistics.models import Department, Area
from django.db.models.signals import post_save
from cvn.models import CVN


def update_statistics(instance, **kwargs):
    user = instance.user_profile.user
    (dept, dept_json) = Department.get_user_unit(
        rrhh_code=user.profile.rrhh_code)
    if dept is not None and dept_json is not None:
        dept.update(dept_json['unidad']['nombre'],
                    dept_json['miembros'], commit=True)
    (area, area_json) = Area.get_user_unit(
        rrhh_code=user.profile.rrhh_code)
    if area is not None and area_json is not None:
        area.update(area_json['unidad']['nombre'],
                    area_json['miembros'], commit=True)
    request = CrequestMiddleware.get_request()
    send_department(request, user)
    send_area(request, user)

post_save.connect(update_statistics, sender=CVN,
                  dispatch_uid='update_statistics')


def send_department(request, user):
    if request:
        dept = Department.get_user_unit(rrhh_code=user.profile.rrhh_code)[0]
        if dept is not None:
            request.session['dept_name'] = dept.name


def send_area(request, user):
    if request:
        area = Area.get_user_unit(rrhh_code=user.profile.rrhh_code)[0]
        if area is not None:
            request.session['area_name'] = area.name


def info_to_session(user, **kwargs):
    request = CrequestMiddleware.get_request()
    send_department(request, user)
    send_area(request, user)

user_logged_in.connect(info_to_session, dispatch_uid='info_to_session')
