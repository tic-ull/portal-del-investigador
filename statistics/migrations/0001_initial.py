# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40, verbose_name='Name')),
                ('code', models.CharField(max_length=10, verbose_name='Unit code')),
                ('number_valid_cvn', models.IntegerField(verbose_name='Valid CVN ')),
                ('computable_members', models.IntegerField(verbose_name='Computable members')),
                ('total_members', models.IntegerField(verbose_name='Total members')),
                ('percentage', models.DecimalField(verbose_name='Percentage valid CVN', max_digits=5, decimal_places=2)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40, verbose_name='Name')),
                ('code', models.CharField(max_length=10, verbose_name='Unit code')),
                ('number_valid_cvn', models.IntegerField(verbose_name='Valid CVN ')),
                ('computable_members', models.IntegerField(verbose_name='Computable members')),
                ('total_members', models.IntegerField(verbose_name='Total members')),
                ('percentage', models.DecimalField(verbose_name='Percentage valid CVN', max_digits=5, decimal_places=2)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProfessionalCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10, verbose_name='Category code')),
                ('name', models.CharField(max_length=255, verbose_name='Category')),
                ('is_cvn_required', models.NullBooleanField(verbose_name='CVN required')),
            ],
            options={
                'verbose_name_plural': 'Professional categories',
            },
            bases=(models.Model,),
        ),
    ]
