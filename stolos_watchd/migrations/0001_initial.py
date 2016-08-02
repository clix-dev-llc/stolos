# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 15:18
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectRoutingConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=256)),
                ('config', django.contrib.postgres.fields.jsonb.JSONField()),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='routing_config', to='projects.Project')),
            ],
        ),
    ]
