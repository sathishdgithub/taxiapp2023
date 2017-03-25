# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0014_auto_20170325_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxi_detail',
            name='date_of_birth',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='date_of_validity',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='insurance',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='taxi_detail',
            name='pollution',
            field=models.DateField(null=True, blank=True),
        ),
    ]
