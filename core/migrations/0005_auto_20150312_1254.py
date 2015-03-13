# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_readonly_staff_permission(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    content_type = ContentType.objects.get(app_label='auth', model='user')
    Permission.objects.create(content_type=content_type,
                              codename='readonly_staff',
                              name='Can acces readonly admin panel')


def delete_readonly_staff_permission(apps, schema_editor):
    apps.get_model('auth.Permission').objects.get(
        codename='readonly_staff').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150114_0936'),
    ]

    operations = [
        migrations.RunPython(add_readonly_staff_permission,
                             delete_readonly_staff_permission),
    ]