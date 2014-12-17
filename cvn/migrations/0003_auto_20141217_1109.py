# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fill_uploaded_at(apps, schema_editor):
    cvns = apps.get_model("cvn", "CVN").objects.all()
    for cvn in cvns:
        cvn.uploaded_at = cvn.updated_at
        cvn.save()


def unfill_uploaded_at(apps, schema_editor):
    """We allow it to be reversible, but there is no need to do anything
       because the values before the migration are garbage"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cvn', '0002_auto_20141217_1109'),
    ]

    operations = [
        migrations.RunPython(fill_uploaded_at, unfill_uploaded_at),
    ]
