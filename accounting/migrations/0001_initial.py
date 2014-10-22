# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Convenio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50, verbose_name='Code')),
                ('igualdad_genero', models.NullBooleanField(default=None, verbose_name='Igualdad de g\xe9nero')),
                ('software_libre', models.NullBooleanField(default=None, verbose_name='Software libre')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name_plural': 'Agreements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50, verbose_name='Code')),
                ('igualdad_genero', models.NullBooleanField(default=None, verbose_name='Igualdad de g\xe9nero')),
                ('software_libre', models.NullBooleanField(default=None, verbose_name='Software libre')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name_plural': 'Projects',
            },
            bases=(models.Model,),
        ),
    ]
