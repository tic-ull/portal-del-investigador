# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_extra_users(apps, schema_editor):
    user = apps.get_model("auth.User").objects.create(username='GesInv-ULL')
    apps.get_model("core", "UserProfile").objects.create(user=user,
                                                         documento='00000000A')


def delete_extra_users(apps, schema_editor):
    user = apps.get_model("auth.User").objects.get(username='GesInv-ULL')
    apps.get_model("core", "UserProfile").objects.get(user=user).delete()
    user.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_extra_users, delete_extra_users),
    ]
