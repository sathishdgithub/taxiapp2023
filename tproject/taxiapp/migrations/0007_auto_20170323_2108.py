# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0006_auto_20170323_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint_statement',
            name='reason',
            field=models.CharField(default='R1', max_length=2, choices=[('R1', 'I was involved in an accident.'), ('R2', 'I lost an item.'), ('R3', 'I would like a refund.'), ('R4', 'My driver was unprofessional'), ('R5', 'My vehicle was not what I expected.'), ('R6', 'I cannot request a ride.'), ('R7', 'I have a different issue.')]),
        ),
        migrations.AddField(
            model_name='complaint_statement',
            name='taxi',
            field=models.ForeignKey(to='taxiapp.Taxi_Detail', null=True),
        ),
        migrations.AlterField(
            model_name='complaint_statement',
            name='complaint',
            field=models.CharField(max_length=200),
        ),
    ]
