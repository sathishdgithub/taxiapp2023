# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 05:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0003_auto_20170323_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxi_detail',
            name='driver_image',
            field=models.ImageField(default='media/default_qr.png', upload_to='drivers'),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='qr_image',
            field=models.ImageField(default='media/default_qr.png', upload_to='qr'),
        ),
    ]
