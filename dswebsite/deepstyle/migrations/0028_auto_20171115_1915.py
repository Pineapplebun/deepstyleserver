# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-15 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deepstyle', '0027_auto_20171115_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='input_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='job',
            name='style_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]