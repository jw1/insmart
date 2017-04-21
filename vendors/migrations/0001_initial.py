# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=' ', max_length=100)),
                ('website_address', models.CharField(default='', max_length=200)),
                ('contact_name', models.CharField(default='', max_length=100)),
                ('contact_email', models.CharField(default='', max_length=100)),
                ('contact_phone', models.CharField(default='', max_length=100)),
                ('physical_address_line_1', models.CharField(default='', max_length=100)),
                ('physical_address_line_2', models.CharField(default='', max_length=100)),
                ('physical_address_city', models.CharField(default='', max_length=100)),
                ('physical_address_state', models.CharField(default='', max_length=50)),
                ('physical_address_postal_code', models.CharField(default='', max_length=25)),
                ('physical_address_country', models.CharField(default='', max_length=50)),
                ('mailing_address_line_1', models.CharField(default='', max_length=100)),
                ('mailing_address_line_2', models.CharField(default='', max_length=100)),
                ('mailing_address_state', models.CharField(default='', max_length=50)),
                ('mailing_address_postal_code', models.CharField(default='', max_length=25)),
                ('mailing_address_country', models.CharField(default='', max_length=50)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]