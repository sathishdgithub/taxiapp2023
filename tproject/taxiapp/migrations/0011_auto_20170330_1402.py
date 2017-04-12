# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0010_auto_20170330_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxi_detail',
            name='aadhar_number',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='autostand',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='capacity_of_passengers',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='chasis_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='driving_license_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='engine_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='owner_driver',
            field=models.CharField(blank=True, choices=[('Owner', 'Owner'), ('Driver', 'Driver')], default='Owner', max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='union',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]