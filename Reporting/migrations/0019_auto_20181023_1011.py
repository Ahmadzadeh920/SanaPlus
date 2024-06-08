# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-23 06:41
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reporting', '0018_auto_20181021_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manage_Device',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Events_id', models.IntegerField()),
                ('date_visited', models.DateTimeField()),
                ('json_fields', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='PageRank',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Events_id', models.IntegerField()),
                ('date_visited', models.DateTimeField()),
                ('json_fields', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Events_id', models.IntegerField()),
                ('date_reserve', models.DateTimeField()),
                ('json_fields', django.contrib.postgres.fields.jsonb.JSONField()),
                ('Reservation_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sell',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Events_id', models.IntegerField()),
                ('date_sell', models.DateTimeField()),
                ('json_fields', django.contrib.postgres.fields.jsonb.JSONField()),
                ('Reservation_id', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='ManageDevice',
        ),
        migrations.DeleteModel(
            name='PageRanking',
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
        migrations.DeleteModel(
            name='seller',
        ),
    ]
