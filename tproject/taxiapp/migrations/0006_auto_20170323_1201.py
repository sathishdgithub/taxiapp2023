# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 06:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0005_auto_20170323_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taxi_detail',
            old_name='qr_image',
            new_name='qrcode',
        ),
    ]
