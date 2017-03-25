# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0012_auto_20170325_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxi_detail',
            name='aadhar_number',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='date_of_birth',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='date_of_validity',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='insurance',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='pollution',
            field=models.DateField(blank=True),
        ),
    ]
