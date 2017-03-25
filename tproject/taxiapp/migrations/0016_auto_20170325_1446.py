# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0015_auto_20170325_1443'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taxi_detail',
            old_name='s_o_of',
            new_name='son_of',
        ),
    ]
