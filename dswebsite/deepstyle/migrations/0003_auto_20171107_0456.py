# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-07 04:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deepstyle', '0002_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_completed',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_start',
            field=models.DateTimeField(),
        ),
    ]
