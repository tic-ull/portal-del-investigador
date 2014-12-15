# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20141008_0853'),
        ('cvn', '0003_auto_20141212_1213'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldCvnPdf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cvn_file', models.FileField(upload_to=b'cvn/old_cvn', verbose_name='PDF')),
                ('uploaded_at', models.DateTimeField(verbose_name='Uploaded PDF')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('user_profile', models.ForeignKey(to='core.UserProfile')),
            ],
            options={
                'ordering': ['-uploaded_at'],
                'verbose_name_plural': 'Hist\xf3rico de Curr\xedculum Vitae Normalizado',
            },
            bases=(models.Model,),
        ),
    ]
