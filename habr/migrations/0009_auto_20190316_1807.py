# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-03-16 15:07
from __future__ import unicode_literals

from django.db import migrations, models
import habr.models


class Migration(migrations.Migration):

    dependencies = [
        ('habr', '0008_auto_20190316_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=habr.models.generic_filename),
        ),
    ]
