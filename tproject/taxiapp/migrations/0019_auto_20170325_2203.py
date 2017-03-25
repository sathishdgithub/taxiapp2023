# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0018_auto_20170325_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_complaint',
            name='admin_id',
        ),
        migrations.RemoveField(
            model_name='user_complaint',
            name='complaint_id',
        ),
        migrations.RemoveField(
            model_name='user_complaint',
            name='taxi_id',
        ),
        migrations.AddField(
            model_name='myuser',
            name='address',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='sms_number',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='whatsapp_number',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='date_of_birth',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='Admin_Detail',
        ),
        migrations.DeleteModel(
            name='User_Complaint',
        ),
    ]
