# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 06:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0004_auto_20170323_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxi_detail',
            name='qr_image',
            field=models.ImageField(blank=True, null=True, upload_to='qr'),
        ),
    ]
