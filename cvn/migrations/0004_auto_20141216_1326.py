# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cvn', '0003_auto_20141212_1213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='convenio',
            options={'verbose_name_plural': 'Agreements'},
        ),
        migrations.AlterModelOptions(
            name='proyecto',
            options={'verbose_name_plural': 'Projects'},
        ),
        migrations.AddField(
            model_name='convenio',
            name='numero_de_investigadores',
            field=models.IntegerField(null=True, verbose_name='Number of researchers', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='convenio',
            name='ambito',
            field=models.CharField(max_length=50, null=True, verbose_name='\xc1mbito', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='convenio',
            name='cod_segun_financiadora',
            field=models.CharField(max_length=150, null=True, verbose_name='Code acc. to the funding institution', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='convenio',
            name='titulo',
            field=models.CharField(max_length=1000, null=True, verbose_name='Designation', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='ambito',
            field=models.CharField(max_length=50, null=True, verbose_name='\xc1mbito', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='titulo',
            field=models.CharField(max_length=1000, null=True, verbose_name='Designation', blank=True),
            preserve_default=True,
        ),
    ]
