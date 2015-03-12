# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_view_permission_to_userprofile(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    model_name = 'userprofile'
    content_type = ContentType.objects.get(model=model_name)

    Permission.objects.create(content_type=content_type,
                              codename='view_' + model_name,
                              name='Can view ' + model_name)


def delete_view_permission_from_userprofile(apps, schema_editor):
    apps.get_model('auth.Permission').objects.get(
        codename='view_userprofile').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150114_0936'),
    ]

    operations = [
        migrations.RunPython(add_view_permission_to_userprofile,
                             delete_view_permission_from_userprofile),
    ]