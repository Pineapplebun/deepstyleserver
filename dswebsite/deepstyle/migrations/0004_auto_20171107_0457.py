# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-07 04:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deepstyle', '0003_auto_20171107_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_completed',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_start',
            field=models.DateTimeField(blank=True),
        ),
    ]
