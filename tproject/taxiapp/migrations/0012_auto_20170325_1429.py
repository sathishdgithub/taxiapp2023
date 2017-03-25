# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0011_auto_20170325_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxi_detail',
            name='chasis_number',
            field=models.CharField(default='default', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='engine_number',
            field=models.CharField(default='default', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='owner_driver',
            field=models.CharField(default='Owner', max_length=6, choices=[('Owner', 'Owner'), ('Driver', 'Driver')]),
        ),
        migrations.AddField(
            model_name='taxi_detail',
            name='pollution',
            field=models.DateField(default=datetime.datetime(2017, 3, 25, 8, 59, 20, 372213, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
