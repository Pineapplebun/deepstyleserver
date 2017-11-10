# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-10 04:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deepstyle', '0014_auto_20171109_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='job',
            name='input_image',
            field=models.ForeignKey(null='False', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='deepstyle.Image'),
        ),
        migrations.AlterField(
            model_name='job',
            name='output_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]