# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0008_auto_20170323_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint_statement',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]
