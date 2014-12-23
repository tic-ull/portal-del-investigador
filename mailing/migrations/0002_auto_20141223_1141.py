# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from mailing import settings as st_mail


def create_email_expired(apps, schema_editor):
    apps.get_model("mailing", "Email").objects.create(
        entry_type=st_mail.MailType.EXPIRED.value)


def delete_email_expired(apps, schema_editor):
    apps.get_model("mailing", "Email").objects.get(
        entry_type=st_mail.MailType.EXPIRED.value).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_email_expired, delete_email_expired),
    ]
