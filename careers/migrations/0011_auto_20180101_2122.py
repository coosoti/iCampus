# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-01 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0010_auto_20180101_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
