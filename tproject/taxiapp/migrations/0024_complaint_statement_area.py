# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0023_auto_20170328_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint_statement',
            name='area',
            field=models.CharField(default='Hyderabad', max_length=200),
            preserve_default=False,
        ),
    ]
