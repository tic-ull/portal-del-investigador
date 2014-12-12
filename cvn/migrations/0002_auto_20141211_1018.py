# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cvn', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patente',
            options={'ordering': ['-fecha', 'titulo'], 'verbose_name_plural': 'Intellectual Properties'},
        ),
        migrations.AddField(
            model_name='cvn',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 11, 10, 18, 1, 314355), verbose_name='PDF Subido'),
            preserve_default=True,
        ),
    ]
