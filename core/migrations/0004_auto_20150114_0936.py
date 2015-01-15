# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20141223_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='entry_type',
            field=models.IntegerField(verbose_name='Type', choices=[(0, b'CVN_STATUS'), (1, b'AUTH_ERROR'), (2, b'EMAIL_SENT'), (3, b'CVN_UPDATED')]),
            preserve_default=True,
        ),
    ]
