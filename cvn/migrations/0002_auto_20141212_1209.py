# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import cvn.helpers


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
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 18, 0, 0), verbose_name='Uploaded PDF'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cvn',
            name='cvn_file',
            field=models.FileField(upload_to=cvn.helpers.get_cvn_path, verbose_name='PDF'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cvn',
            name='xml_file',
            field=models.FileField(upload_to=cvn.helpers.get_cvn_path, verbose_name='XML'),
            preserve_default=True,
        ),
    ]
