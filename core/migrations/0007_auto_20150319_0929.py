# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.contenttypes.management import update_all_contenttypes


def add_staff_menu_permission(apps, schema_editor):
    update_all_contenttypes()  # Fixes tests
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    content_type = ContentType.objects.get(app_label='auth', model='user')
    Permission.objects.create(content_type=content_type,
                              codename='read_admin_menu',
                              name='Can read Admin Menu')


def delete_staff_menu_permission(apps, schema_editor):
    apps.get_model('auth.Permission').objects.get(
        codename='read_admin_menu').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150317_1249'),
    ]

    operations = [
        migrations.RunPython(add_staff_menu_permission,
                             delete_staff_menu_permission),
    ]
