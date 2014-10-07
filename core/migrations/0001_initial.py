# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application', models.CharField(max_length=20, verbose_name='Application')),
                ('entry_type', models.IntegerField(verbose_name='Type', choices=[(0, b'CVN_STATUS'), (1, b'AUTH_ERROR')])),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('message', models.TextField(verbose_name='Message')),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('documento', models.CharField(unique=True, max_length=20, verbose_name='Document')),
                ('rrhh_code', models.CharField(max_length=20, unique=True, null=True, verbose_name='Person code', blank=True)),
                ('user', models.OneToOneField(related_name=b'profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__username'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='log',
            name='user_profile',
            field=models.ForeignKey(blank=True, to='core.UserProfile', null=True),
            preserve_default=True,
        ),
    ]
