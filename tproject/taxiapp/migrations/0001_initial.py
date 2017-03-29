# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 18:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import location_field.models.plain


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_number', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('sms_number', models.IntegerField()),
                ('address', models.CharField(blank=True, max_length=200)),
                ('location', location_field.models.plain.PlainLocationField(blank=True, max_length=63, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City_Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=40)),
                ('city_code', models.CharField(max_length=10)),
                ('taxi_no', models.IntegerField(default=0)),
                ('police_no', models.IntegerField(default=1)),
                ('complaint_no', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Complaint_Statement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint_number', models.CharField(max_length=10)),
                ('area', models.CharField(max_length=200)),
                ('complaint', models.CharField(blank=True, max_length=100, null=True)),
                ('resolved', models.BooleanField(default=False)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxiapp.City_Code')),
            ],
        ),
        migrations.CreateModel(
            name='Reasons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Taxi_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_plate', models.CharField(max_length=20)),
                ('traffic_number', models.CharField(max_length=20)),
                ('driver_name', models.CharField(max_length=40)),
                ('son_of', models.CharField(max_length=40)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('phone_number', models.CharField(max_length=13)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('aadhar_number', models.CharField(max_length=14)),
                ('driving_license_number', models.CharField(max_length=30)),
                ('date_of_validity', models.DateField(blank=True, null=True)),
                ('autostand', models.CharField(max_length=80)),
                ('union', models.CharField(max_length=100)),
                ('insurance', models.DateField(blank=True, null=True)),
                ('capacity_of_passengers', models.CharField(max_length=10)),
                ('pollution', models.DateField(blank=True, null=True)),
                ('engine_number', models.CharField(max_length=20)),
                ('chasis_number', models.CharField(max_length=20)),
                ('owner_driver', models.CharField(choices=[('Owner', 'Owner'), ('Driver', 'Driver')], default='Owner', max_length=6)),
                ('num_of_complaints', models.IntegerField(default=0)),
                ('driver_image', models.ImageField(default='drivers/profile.png', upload_to='drivers')),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxiapp.City_Code')),
            ],
        ),
        migrations.AddField(
            model_name='complaint_statement',
            name='reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxiapp.Reasons'),
        ),
        migrations.AddField(
            model_name='complaint_statement',
            name='taxi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='taxiapp.Taxi_Detail'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxiapp.City_Code'),
        ),
    ]
