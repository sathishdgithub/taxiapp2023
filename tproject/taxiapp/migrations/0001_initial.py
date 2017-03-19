# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_Details',
            fields=[
                ('admin_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('sms_number', models.IntegerField()),
                ('whatsapp_number', models.IntegerField()),
                ('address', models.CharField(max_length=200, blank=True)),
                ('coordinate_x', models.IntegerField()),
                ('coordinate_y', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Complaint_Statements',
            fields=[
                ('complaint_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('complaint', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Login_Details',
            fields=[
                ('user_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=100)),
                ('access_level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('date_of_birth', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Taxi_Details',
            fields=[
                ('taxi_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('number_plate', models.CharField(max_length=20)),
                ('driver_name', models.CharField(max_length=40)),
                ('web_page_url', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('phone_number', models.IntegerField()),
                ('other_details', models.CharField(max_length=200, blank=True)),
                ('num_of_complaints', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User_Complaint',
            fields=[
                ('complaint_number', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('user_locations_x', models.IntegerField()),
                ('user_locations_y', models.IntegerField()),
                ('admin_id', models.ForeignKey(to='taxiapp.Admin_Details')),
                ('complaint_id', models.ForeignKey(to='taxiapp.Complaint_Statements')),
                ('taxi_id', models.ForeignKey(to='taxiapp.Taxi_Details')),
            ],
        ),
    ]
