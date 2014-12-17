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
            name='articulo',
            options={'ordering': ['-fecha', 'titulo'], 'verbose_name_plural': 'Articles'},
        ),
        migrations.AlterModelOptions(
            name='capitulo',
            options={'ordering': ['-fecha', 'titulo'], 'verbose_name_plural': 'Chapters of books'},
        ),
        migrations.AlterModelOptions(
            name='cvn',
            options={'ordering': ['-uploaded_at', '-updated_at'], 'verbose_name_plural': 'Normalized Curriculum Vitae'},
        ),
        migrations.AlterModelOptions(
            name='libro',
            options={'ordering': ['-fecha', 'titulo'], 'verbose_name_plural': 'Books'},
        ),
        migrations.AlterModelOptions(
            name='patente',
            options={'ordering': ['-fecha', 'titulo'], 'verbose_name_plural': 'Intellectual Properties'},
        ),
        migrations.AddField(
            model_name='convenio',
            name='numero_de_investigadores',
            field=models.IntegerField(null=True, verbose_name='Number of researchers', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cvn',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 18, 0, 0), verbose_name='Uploaded PDF'),
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
