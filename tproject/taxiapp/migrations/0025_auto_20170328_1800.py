# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0024_complaint_statement_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxi_detail',
            name='driver_image',
            field=models.ImageField(default='drivers/profile.png', upload_to='drivers'),
        ),
    ]