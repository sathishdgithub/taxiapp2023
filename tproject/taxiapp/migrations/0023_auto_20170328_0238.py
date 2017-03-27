# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0022_auto_20170327_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint_statement',
            name='complaint',
            field=models.CharField(max_length=100),
        ),
    ]
