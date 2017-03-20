# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxiapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sms_number', models.IntegerField()),
                ('whatsapp_number', models.IntegerField()),
                ('address', models.CharField(max_length=200, blank=True)),
                ('coordinate_x', models.IntegerField()),
                ('coordinate_y', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Complaint_Statement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complaint', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Taxi_Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_plate', models.CharField(max_length=20)),
                ('driver_name', models.CharField(max_length=40)),
                ('web_page_url', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('phone_number', models.IntegerField()),
                ('other_details', models.CharField(max_length=200, blank=True)),
                ('num_of_complaints', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Login_Details',
        ),
        migrations.RemoveField(
            model_name='user_complaint',
            name='complaint_number',
        ),
        migrations.AddField(
            model_name='user_complaint',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=2, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user_complaint',
            name='admin_id',
            field=models.ForeignKey(to='taxiapp.Admin_Detail'),
        ),
        migrations.AlterField(
            model_name='user_complaint',
            name='complaint_id',
            field=models.ForeignKey(to='taxiapp.Complaint_Statement'),
        ),
        migrations.AlterField(
            model_name='user_complaint',
            name='taxi_id',
            field=models.ForeignKey(to='taxiapp.Taxi_Detail'),
        ),
        migrations.DeleteModel(
            name='Admin_Details',
        ),
        migrations.DeleteModel(
            name='Complaint_Statements',
        ),
        migrations.DeleteModel(
            name='Taxi_Details',
        ),
    ]
