# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 08:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0009_auto_20170330_1354'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='complaint_statement',
            options={'verbose_name': 'Customer Complaint', 'verbose_name_plural': 'Customer Complaints'},
        ),
        migrations.AlterModelOptions(
            name='myuser',
            options={'verbose_name': 'Administrator', 'verbose_name_plural': 'Administrators'},
        ),
        migrations.AlterModelOptions(
            name='reasons',
            options={'verbose_name': 'Complaint Reason', 'verbose_name_plural': 'Complaint Reasons'},
        ),
        migrations.AlterModelOptions(
            name='taxi_detail',
            options={'verbose_name': 'Taxi Driver', 'verbose_name_plural': 'Taxi Drivers'},
        ),
    ]