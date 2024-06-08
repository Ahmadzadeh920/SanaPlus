# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-17 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reporting', '0008_manage_device'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManageDevice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Events_id', models.IntegerField()),
                ('Os_family', models.CharField(max_length=100)),
                ('Os_version', models.CharField(max_length=100)),
                ('browser_family', models.CharField(max_length=100)),
                ('device_family', models.CharField(max_length=100)),
                ('date_visited', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='manage_device',
        ),
    ]
