# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.contenttypes.management import update_all_contenttypes


def add_impersonate_permission(apps, schema_editor):
    update_all_contenttypes()  # Fixes tests
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    content_type = ContentType.objects.get(app_label='auth', model='user')
    Permission.objects.create(content_type=content_type,
                              codename='impersonate',
                              name='Can impersonate other user')


def delete_impersonate_permission(apps, schema_editor):
    apps.get_model('auth.Permission').objects.get(
        codename='impersonate').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150319_0929'),
    ]

    operations = [
        migrations.RunPython(add_impersonate_permission,
                             delete_impersonate_permission),
    ]