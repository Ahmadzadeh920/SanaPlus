# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-03 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reporting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clicked_Events_varchar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('json_format', models.TextField()),
                ('date_visited', models.DateField()),
            ],
        ),
    ]
