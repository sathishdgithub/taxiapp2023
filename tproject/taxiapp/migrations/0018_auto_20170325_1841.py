# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0017_auto_20170325_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin_detail',
            name='city',
            field=models.CharField(default='Hyderabad', max_length=255),
        ),
        migrations.AddField(
            model_name='admin_detail',
            name='location',
            field=location_field.models.plain.PlainLocationField(max_length=63, null=True, blank=True),
        ),
    ]
