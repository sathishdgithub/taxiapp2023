# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0010_auto_20170324_2139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taxi_detail',
            old_name='qr_code',
            new_name='qrcode',
        ),
        migrations.RemoveField(
            model_name='taxi_detail',
            name='other_details',
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='aadhar_number',
            field=models.CharField(default='default', max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='autostand',
            field=models.CharField(default='default', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='capacity_of_passengers',
            field=models.CharField(default='default', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2017, 3, 25, 8, 49, 15, 246619, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='date_of_validity',
            field=models.DateField(default=datetime.datetime(2017, 3, 25, 8, 49, 23, 118375, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='driving_license_number',
            field=models.CharField(default='default', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='insurance',
            field=models.DateField(default=datetime.datetime(2017, 3, 25, 8, 49, 46, 950023, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='s_o_of',
            field=models.CharField(default='default', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='traffic_number',
            field=models.CharField(default='default', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='union',
            field=models.CharField(default='default', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='address',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='phone_number',
            field=models.CharField(max_length=13),
        ),
    ]
