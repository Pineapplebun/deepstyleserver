# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-09 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deepstyle', '0013_auto_20171109_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='input_image',
            field=models.FileField(null='False', upload_to=''),
        ),
    ]
