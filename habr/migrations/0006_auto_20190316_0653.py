# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-03-16 03:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('habr', '0005_auto_20190316_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
