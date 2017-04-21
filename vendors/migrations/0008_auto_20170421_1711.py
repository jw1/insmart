# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-21 22:11
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0007_auto_20170421_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='website_address',
            field=models.CharField(default='', max_length=200, validators=[django.core.validators.URLValidator()]),
        ),
    ]