# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=100, verbose_name='Code')),
                ('gender_equality', models.NullBooleanField(default=None, verbose_name='Igualdad de g\xe9nero')),
                ('free_software', models.NullBooleanField(default=None, verbose_name='Software Libre')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'ordering': ['-code'],
                'verbose_name_plural': 'Agreements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=100, verbose_name='Code')),
                ('gender_equality', models.NullBooleanField(default=None, verbose_name='Igualdad de g\xe9nero')),
                ('free_software', models.NullBooleanField(default=None, verbose_name='Software Libre')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'ordering': ['-code'],
                'verbose_name_plural': 'Projects',
            },
            bases=(models.Model,),
        ),
    ]
